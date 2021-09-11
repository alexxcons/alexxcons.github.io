---
layout: post
title:  "Shiny new things in Thunar thanks to GSoC 2021"
date:   2021-09-11 14:50:00
tags: Xfce Thunar GSoC
comments: true
---

[GSoC 2021](https://summerofcode.withgoogle.com) is over now and I am happy to tell you that both students working on thunar did an excellent job. Alot of nice stuff has been added thanks to them !

In order to allow you to discover all these new features [Thunar 4.17.5](https://mail.xfce.org/pipermail/xfce-announce/2021-September/001059.html) was just released.
(Note that this is a development release. It still might have some rough edges)

For details about the new features check the summaries provided by Sergios and Yongha:

[Sergios GSoC Summary](http://users.uoa.gr/~sdi1800073/sources/xfce_blog05.html)

[Yongha's GSoC Summary](https://dev.ikx.kr/GSOC-6th/)

As well here some more new features added during GSoC for which I thought they would be worth to mention:

<hr>
Bookmarks got moved into a separate 'Bookmarks Menu' and a 'create bookmark' option was added
([MR !109](https://gitlab.xfce.org/xfce/thunar/-/merge_requests/109) and [MR !71](https://gitlab.xfce.org/xfce/thunar/-/merge_requests/71))

![bookmark menu](/assets/img/bookmark_menu.png)

<hr>
Better discover discoverability for setting default applications:

A new menu item "Set Default Application" was added to the "Open with" submenu ([MR !79](https://gitlab.xfce.org/xfce/thunar/-/merge_requests/79))

![Open with - Set Default App](/assets/img/default_app_1.png)

<hr>
A new section 'Default Application' was added to the 'thunar-chooser-dialog' ([MR !81]((https://gitlab.xfce.org/xfce/thunar/-/merge_requests/81)))  

![Default App Section](/assets/img/default_app_2.png)

<hr>
On top there are still [various open merge requests](https://gitlab.xfce.org/xfce/thunar/-/merge_requests) with partial finished features, most of them from GSoC students for which I did not find time so far.
So expect more new stuff to arrive soon !

You as well might want to keep an eye on [xfce4-terminal](https://gitlab.xfce.org/apps/xfce4-terminal), which received alot of activity recently, since it is now maintained by Sergios Kefalidis.

If you find a bug on any of these new features, please make use of the xfce bugtracker.

Happy testing ! 
