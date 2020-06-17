---
layout: post
title:  "Thunar, GtkAction and a big mess"
date:   2020-06-04 22:51:00
tags: Xfce Thunar
comments: true
---

### Overview

My journey into the [GtkAction](https://developer.gnome.org/gtk3/stable/GtkAction.html) abysses of [Thunar](https://gitlab.xfce.org/xfce/thunar) began in the mid of 2019. Be warned, it is no story of success. It is rather a story about finding a way through a maze while walking into almost every dead end.

Actually I just wanted to fix [#198 (Merge all file-context-menus into one)](https://gitlab.xfce.org/xfce/thunar/-/issues/198). But somehow things got weird. More than half a year later and after numerous interactive rebases I finally merged my branch into master \o/

### Motivation

The old Thunar used to create the same menu items in different places using different code. In the past that led to inconsistencies. E.g. the location bar only provided a very minimal context menu, no [custom actions](https://docs.xfce.org/xfce/thunar/custom-actions) at all.

![location button context menu](/assets/img/location_buttons_context_menu.png)

From time to time I found myself right-clicking on a `location-button`, just to find out that there still is no `custom action`. At some point of maximal annoyance I decided to fix that problem ... not sure if I would have done so when I knew how long that road would be.

Looking at [thunar-location-buttons.c](https://gitlab.xfce.org/xfce/thunar/-/blob/xfce-4.14/thunar/thunar-location-button.c) revealed a lot of duplicated code. [thunar-standard-view](https://gitlab.xfce.org/xfce/thunar/-/blob/xfce-4.14/thunar/thunar-standard-view.c) and [thunar-window](https://gitlab.xfce.org/xfce/thunar/-/blob/xfce-4.14/thunar/thunar-window.c) both used the deprecated [GtkActionEntry](https://developer.gnome.org/gtk3/stable/GtkActionGroup.html#GtkActionEntry) to define `menu item labels` and related actions. The `location buttons` just mirrored parts of that code. On top some other actions were defined in [thunar-launcher](https://gitlab.xfce.org/xfce/thunar/-/blob/xfce-4.14/thunar/thunar-standard-view.c) or had their own classes, inheriting `GtkAction`.

So yay, lets just copy+paste the missing stuff to the location buttons?
Nah, that would be too easy. As a developer who values [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself), it would hurt my belief in clean code to produce more mess.

### Let's Start Hacking

I started to do some coding .. first I created a new widget [thunar-menu](https://gitlab.xfce.org/xfce/thunar/-/blob/master/thunar/thunar-menu.c) which internally is a [gtk-menu](https://developer.gnome.org/gtk3/stable/GtkMenu.html), and moved menu-item creation and the related actions for copy/cut/paste/delete/move_to_trash there to have them at some central place, so they can be reused by different menus. I as well moved the actions from `thunar-launcher` to `thunar-menu` (I guess the original intention of the launcher was, to actually launch things, not to manage menu-items) and replaced separate action classes in favour of methods inside `thunar-menu`.

Meanwhile the location-button-menu and the context-menu, which I used for testing, were populated with some items again.

The old code made massive use of the deprecated `GtkAction` and `GtkActionEntry` classes together with `GtkUiManager`. I did not want to add more `G_GNUC_BEGIN_IGNORE_DEPRECATIONS` to silence warnings. So I decided to replace the deprecated calls.

Looking into the gtk3 documentation revealed that there now is [GAction](https://developer.gnome.org/GAction/) and [GActionEntry](https://developer.gnome.org/gio/stable/GActionMap.html#GActionEntry) which provides some service around accelerator activation, and there is [GtkMenu](https://developer.gnome.org/gtk3/stable/GtkMenu.html)/[GMenu](https://developer.gnome.org/gio/stable/GMenu.html) for which at that time I had no clear idea why there are two of them.

The [documentation of GAction](https://developer.gnome.org/GAction/) told me that it should not be used for anything related to labels, icons or creation of visual widgets, damn. So at that time I did not see an advantage in using this class. I decided to rather go for `GtkMenu` together with some custom replacement for `GtkActionEntry`: [XfceGtkActionEntry](https://gitlab.xfce.org/xfce/libxfce4ui/-/blob/master/libxfce4ui/xfce-gtk-extensions.h#L45).

In retrospective ignoring `GAction` might not have been my smartest move. Meanwhile I understood how `GAction` can be used with `GtkMenu`, and I will most likely go for it at some later point.

Regarding [GtkUiManager](https://developer.gnome.org/gtk3/stable/GtkUIManager.html): The definition of menu-items of Thunar was scattered across [7 different *-ui.xml files](https://gitlab.xfce.org/xfce/thunar/-/commit/ed46f9c3baa3533629d8c1000511300fb0e6fdd5), making it hard to figure out what belongs together. Because of that I decided to just get rid of the deprecated `GtkUiManager` and create menu-items in the code instead of predefining their order in xml. IMO the usage of xml files might be nice for static GUI's, though for dynamic menu-creation it just introduces unnecessary complexity.

So I started to build `XfceGtkActionEntry` and some support methods.`XfceGtkActionEntry` is a structure which holds labels, tooltips, icons, types, the accelerator paths and callbacks to the related actions. Like `GtkActionEntry` it is just a struct and can be filled in a static way.

Next problem: The menus in Thunar so far did not get destroyed, but were updated whenever the selected items got changed, and got shown when needed. That sounded wrong to me. Why should I want to update menu-items, which can be expensive, while no menu is visible at all ?
There were bugs about menu flickering and slowness while rubber banding/mass select which seem to be related. Since I anyhow needed to touch that part, I decided to build menus only when they need to be shown.

Things went well, I came to the point where I needed some items from `thunar-window`, like the zoom-section and the view-specific settings. As well most file-menu items in the `thunar-window` menu did not work any more since I moved management of them from `thunar-launcher` to` thunar-menu`. So next step clearly was: Introduce `XfceGtkActionEntry` to `thunar-window` ... and than shit hit the fan.

So far the `thunar-window` menu was always present and took care for any accelerator actions. Since my concept was "create menu on request", there was no menu instance which could take care for accelerators any more, leading to dysfunctional accelerator keys, rendering my whole concept as faulty .. aargh.

### Start all over again

After some time of grieve and doubts I fixed the problem by moving most of the code from `thunar-menu` back to `thunar-launcher`, which lifetime is coupled to `thunar-window`.

From now on `thunar-menu` was more or less just an convenience wrapper for `thunar-launcher` ... still useful, but sadly it lost its glory. `thunar-launcher` now builds volatile menu items on request and permanently listens to the related accelerators. Finally accelerators started to work fine, and I was able to continue to fight with the window menu.

I had much more trouble with that menu, too much to tell it here .. however somehow I managed to get it functional, so that it mostly worked like before.

### An unpleasant discovery

Later on, while [reporting a bug against gtk](https://gitlab.gnome.org/GNOME/gtk/-/issues/2375) I learned that the class [gtk_accel_map](https://developer.gnome.org/gtk3/stable/gtk3-Accelerator-Maps.html), which I use as a central part will be deprecated soon ... aargh again. The gtk devs so far just missed to set a deprecation macro. So it seems like I will need to touch the accelerator part again. This time I plan to make use of the [GActionMap](https://developer.gnome.org/gio/stable/GActionMap.html) interface .. going to be a story for another day.

### Testing and open issues

For first testing and code-review I luckily got support of some early adopters. They found many more defects and regressions which kept me busy a long while. Fortunately nothing concept-breaking was found.

While writing this there are still some regressions I introduced, waiting to get fixed by me before a stable release:
* [Regression: Missing accelerators for bookmark items](https://gitlab.xfce.org/xfce/thunar/-/issues/331)
* [GObject-WARNING on closing thunar in some conditions](https://gitlab.xfce.org/xfce/thunar/-/issues/319)

And there are related tasks on my agenda, for which I just did not find the time so far:
* rename `thunar-launcher` to e.g. `thunar-action-manager`
* use `thunar-menu` in `bookmark view`
* use `thunar-menu` in `Tree view`
* many minor things

### Conclusion

Finally I ended up with [25 commits and +4717 / -7149 line changes](https://gitlab.xfce.org/xfce/thunar/-/merge_requests/10). The occurrence of `G_GNUC_BEGIN_IGNORE_DEPRECATIONS` got reduced from 250 to 35. The remaining 35 occurrences will further drop when using GtkMenu for bookmark-view/tree-view. That should simplify the move to gtk4 in the future. The `location-button` context menu shows custom-actions now, and as well some other bugs got fixed with the changes.

So overall, the result does not look too bad I guess.

Well, this blogpost grew by far too long. I hope you nevertheless enjoyed the journey into the Thunar internals!

... enough storytelling for now, I really need to take care of these remaining regressions! :)

Thanks to [Reuben](https://gitlab.xfce.org/reubengreen73), [AndreLDM](https://gitlab.xfce.org/andreldm), [DarkTrick](https://gitlab.xfce.org/DarkTrick) and others for early testing and bug reporting! Special thanks to AndreLDM, motivating me to write this blogpost at all :D.