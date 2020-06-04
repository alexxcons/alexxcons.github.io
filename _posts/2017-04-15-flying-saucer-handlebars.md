---
layout: post
title:  "Generate PDFs with Flying Saucer + Handlebars.java"
date:   2017-04-15 23:45:00
tags: pdf handlebars java
---
When it comes to generate PDFs using Java the de facto solution is Jasper Reports. Even though it provides a bunch of features and a great set of tools, such as iReport and JasperSoft Studio, the developer might want a simpler and flexible alternative.
Recently I was involved in a project where I had to craft reports but I felt that using iReport was getting more and more kludgy and messy with lots of subreports. Then I gave Flying Saucer a try and never looked back. For the template engine Handlebars.java was chosen due to its simplicity and my previous experience with Handlebars.js. The combination proved to be awesome!

In this tutorial we are going to build an application that renders a report of purchases by customers to illustrate how simple and powerful is the Flying Saucer and Handlerbars.java combo.

### Enough talking, show me some code ###

First add the dependencies to your project:

{% highlight xml %}
<dependency>
  <groupId>org.xhtmlrenderer</groupId>
  <artifactId>flying-saucer-core</artifactId>
  <version>9.1.5</version>
</dependency>
<dependency>
  <groupId>org.xhtmlrenderer</groupId>
  <artifactId>flying-saucer-pdf</artifactId>
  <version>9.1.5</version>
</dependency>
<dependency>
  <groupId>com.github.jknack</groupId>
  <artifactId>handlebars</artifactId>
  <version>4.0.6</version>
</dependency>
{% endhighlight %}

or gradle if you will:

{% highlight gradle %}
  compile 'org.xhtmlrenderer:flying-saucer-core:9.1.5'
  compile 'org.xhtmlrenderer:flying-saucer-pdf:9.1.5'
  compile 'com.github.jknack:handlebars:4.0.6'
{% endhighlight %}

Now let's create a couple of POJOs:

{% highlight java %}
public class Customer {
  private Integer id;
  private String name;
  private String address;
  private String phone;
  private String email;
  private LocalDate since;
  private List<Purchase> purchases;

  // gettters & setters
}

public class Purchase {
  private String product;
  private Double value;
  private Integer quantity;
  private LocalDateTime date;

  // gettters & setters
}
{% endhighlight %}

Create the `ReportEngine` class to handle the rendering of reports:

{% highlight java %}
public class ReportEngine {
  private Handlebars handlebars;

  public ReportEngine() {
    // init the Handlebars instance
    handlebars = new Handlebars();
    // register our custom helpers, we'll get to this soon
    handlebars.registerHelpers(new HandlebarsHelpers());
  }

  public void generate(String templateFile, String outputFile, Map<String, Object> data) {
    try (OutputStream output = new FileOutputStream(new File(outputFile))) {
      // load the template (.hbs file) from classpath or an external file
      Template template = handlebars.compile(templateFile);

      // run Handlebars render with the input data
      String mergedTemplate = template.apply(data);
      // create a structured document from the generated HTML
      Document doc = getDocumentBuilder().parse(new ByteArrayInputStream(mergedTemplate.getBytes("UTF-8")));

      // now we take the document and apply the magic of flying saucer to create a PDF file
      ITextRenderer renderer = new ITextRenderer();
      renderer.setDocument(doc, null);
      renderer.layout();
      renderer.createPDF(output);
      renderer.finishPDF();
    } catch (IOException | ParserConfigurationException | SAXException | DocumentException e) {
      e.printStackTrace();
    }
  }

  // we use this method to create a DocumentBuild not so fanatic about XHTML
  private DocumentBuilder getDocumentBuilder() throws ParserConfigurationException {
    DocumentBuilderFactory fac = DocumentBuilderFactory.newInstance();
    fac.setNamespaceAware(false);
    fac.setValidating(false);
    fac.setFeature("http://xml.org/sax/features/namespaces", false);
    fac.setFeature("http://xml.org/sax/features/validation", false);
    fac.setFeature("http://apache.org/xml/features/nonvalidating/load-dtd-grammar", false);
    fac.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
    return fac.newDocumentBuilder();
  }
}
{% endhighlight %}

Handlebars follows the tradition of Mustache, where a template engine should not handle logic. But sometimes that imposes limitations and we end up formatting the input data just to work this around. But don't take me wrong, logic-less template engines are great, because they force us to avoid kludges, ugly hacks and many times keep the business logic away from the presentation layer. So here enters Helpers to keep templates simple, powerful and promote reuse. Here are the ones I used to our example:

{% highlight java %}
public class HandlebarsHelpers {
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");

    public CharSequence formatDateTime(final LocalDateTime date, final Options options) throws IOException {
        return formatter.format(date);
    }

    public CharSequence getYear(final LocalDate date, final Options options) throws IOException {
        return String.valueOf(date.getYear());
    }

    public CharSequence purchasesQty(final Customer c, final Options options) throws IOException {
        Integer qty = c.getPurchases().stream()
                .mapToInt(Purchase::getQuantity)
                .sum();

        return String.valueOf(qty);
    }

    public CharSequence purchasesTotal(final Customer c, final Options options) throws IOException {
        Double sum = c.getPurchases().stream()
                .mapToDouble(Purchase::getValue)
                .sum();

        return NumberFormat.getCurrencyInstance().format(sum);
    }

    public CharSequence formatCurrency(final Double value, final Options options) throws IOException {
        if (value == null) return "";
        return NumberFormat.getCurrencyInstance().format(value);
    }
}
{% endhighlight %}

Then comes the time to write the template using plain HTML and Handlebars:

{% raw %}
```handlebars
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <style>
        html {
            font-family: "Open Sans", sans-serif;
            font-size: 10px;
        }

        @page {
            size: A4;
            margin: 10px;
            padding-top: 32px;

            @top-center { content: element(title); }
            @bottom-right { content: element(footer); }
        }

        .footer { position: running(footer); text-align: right; }
        .pagenumber:before { content: counter(page); }
        .pagecount:before { content: counter(pages); }

        .title {
            display: block;
            margin-top: 10px;
            position: running(title);
            width: 100%;
            text-align: center;
        }

        .customer { page-break-inside: avoid; padding-bottom: 2em; }
        .customer table { width: 100%; border-collapse: collapse; margin-top: 1em; }
        .customer td { border: solid black thin; padding: 0 2px; }
        .customer tr:nth-child(odd) { background-color: #f2f2f2; }
        .customer th { border: solid black thin; text-align: center; background-color: #d4f2cd; }
        .customer td:nth-child(1) { width: 65%; }
        .customer .total-row { font-weight: bold; }
        .customer .total-row td { border: none; background-color: #fff; }
    </style>
</head>
<body>
<!-- put these before any other content -->
<h1 class="title">Purchases by Customer</h1>
<div class="footer">Page <span class="pagenumber"></span> of <span class="pagecount"></span></div>

{{#customers}}
<div class="customer">
    <div>Customer: {{id}} - {{name}}</div>
    <div>Address: {{address}}</div>
    <div>Contact: {{email}} / {{phone}}</div>
    <div>Customer Since: {{getYear since}}</div>
    <table>
        <tr>
            <th>Product Description</th>
            <th>Qty</th>
            <th>Value</th>
            <th>Purchase Date</th>
        </tr>
        {{#purchases}}
        <tr>
            <td>{{product}}</td>
            <td>{{quantity}}</td>
            <td>{{formatCurrency value}}</td>
            <td>{{formatDateTime date}}</td>
        </tr>
        {{/purchases}}
        <tr class="total-row">
            <td class="total">TOTAL</td>
            <td>{{purchasesQty this}}</td>
            <td>{{purchasesTotal this}}</td>
            <td></td>
        </tr>
    </table>
</div>
{{/customers}}

</body>
</html>
```
{% endraw %}

Finally it's time to put it all together:

{% highlight java %}
public class App {
    public static void main(String[] args) {
        List<Customer> customers = IntStream
                .rangeClosed(1, 25)
                .mapToObj(RandomDataGenerator::randomCustomer)
                .sorted(Comparator.comparing(Customer::getName))
                .collect(Collectors.toList());

        Map<String, Object> data = new HashMap<>();
        data.put("customers", customers);

        new ReportEngine().generate("purchases", "report.pdf", data);
    }
}
{% endhighlight %}

And this is our nice and tidy report:
![My helpful screenshot]({{ site.url }}/assets/img/flying-saucer-handlebars-example.png)

Here is the [PDF]({{ site.url }}/assets/pdf/flying-saucer-handlebars-example.pdf){:target="_blank"}.

You can also find this [project at GitHub](https://github.com/andreldm/flying-saucer-handlebars-example){:target="_blank"} if you're lazy enough to copy and paste ;)

**More resources**
* [The Flying Saucer User's Guide](https://flyingsaucerproject.github.io/flyingsaucer/r8/guide/users-guide-R8.html){:target="_blank"}
* [Handlebars.java Tempaltes](https://jknack.github.io/handlebars.java/gettingStarted.html){:target="_blank"}
* [Handlebars.java Helpers](https://jknack.github.io/handlebars.java/helpers.html){:target="_blank"}
