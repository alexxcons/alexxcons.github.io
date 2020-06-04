---
layout: post
title:  "Replacing FLTK Callbacks with Lambdas and Signals"
date:   2016-04-02 11:46:00
tags: FLTK C++ lambdas
---
FLTK is a lightweight GUI toolkit which I use for my [music player](https://github.com/andreldm/kissplayer). It's great due to its simplicity and it can also be statically linked.
Unfortunately the project development is mostly stalled after two failed attempts to rewrite/redesign it (FLTK 2.x and FLTK 3.x).
Nevertheless, the library is still useful, somewhat maintained and the community is also active, so I can still rely on it.

Not long ago I started refactoring my music player, basically decoupling some of its components, removing globals and
making use of libsigc++ for signals and C++ 11 Lambdas. Just for comparison, this is the default approach to handle FLTK events with callbacks:

{% highlight c++ %}
#include <FL/Fl.H>
#include <FL/fl_ask.H>
#include <FL/Fl_Button.H>
#include <FL/Fl_Window.H>

void cb_alert(Fl_Widget* widget, void*)
{
  fl_alert("Thank you!");
}

int main(int argc, char** argv)
{
  Fl_Window* window = new Fl_Window(0,0, 300, 200);
  Fl_Button* button = new Fl_Button(5, 5, 80, 25, "Click me");
  button->callback((Fl_Callback*) cb_alert);

  window->show(0, NULL);

  return Fl::run();
}
{% endhighlight %}

Seemingly simple, but doesn't scale well when you have several small callbacks. It gets more awkward when you're using classes.
Thanks to C++ Lambdas that can be reworked into this:

{% highlight c++ %}
button->callback([](Fl_Widget *w, void *u) {
   fl_alert("Thank you!");
});
{% endhighlight %}

Notice that this is a non-capturing lambda. As I wanted to decouple the components using signals, I didn't bother to
make capturing lambdas work as a Fl_Callback. So here is how things can be handled with Lambdas and Signals:

{% highlight c++ %}
#include <FL/Fl.H>
#include <FL/fl_ask.H>
#include <FL/Fl_Box.H>
#include <FL/Fl_Button.H>
#include <FL/Fl_Window.H>

#include <sigc++/sigc++.h>

static sigc::signal<void> SignalClickMe;
static sigc::signal<void> SignalIncrement;

class WindowTest : public Fl_Window
{
  int counter = 0;
  bool button1_clicked = false;
  Fl_Button* button1;
  Fl_Button* button2;
  Fl_Box* label;

  void onClickMe()
  {
    if (button1_clicked) {
      fl_alert("Stop it, you've clicked me already!");
    } else {
      button1->label("Thank you!");
      button1_clicked = true;
    }
  }

public:
	WindowTest() : Fl_Window(300, 300, 300, 200, "Lambda & Signals")
  {
    button1 = new Fl_Button(5, 5, 80, 25, "Click me");
    button2 = new Fl_Button(5, 70, 80, 25, "Increment");
    label   = new Fl_Box(5, 100, 80, 25, "Counter: 0");

    button1->callback([](Fl_Widget *w, void *u) { SignalClickMe.emit(); });
    button2->callback([](Fl_Widget *w, void *u) { SignalIncrement.emit(); });

    SignalClickMe.connect(sigc::mem_fun(this, &WindowTest::onClickMe));
    SignalIncrement.connect([this] {
      char text[50];
      sprintf(text, "Counter: %d", ++counter);
      label->copy_label(text);
    });
  }
};

int main(int argc, char** argv)
{
  WindowTest* window = new WindowTest();  
  window->show(0, NULL);
  return Fl::run();
}
{% endhighlight %}

That's it, this combination makes possible to decouple the code across other classes and avoid tens or hundred of dangling callbacks.
