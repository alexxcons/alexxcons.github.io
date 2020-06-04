---
layout: post
title:  "The Ultimate Contributor's Guide to Xfce"
date:   2018-12-03 22:20:00
tags: Xfce Open-source
---

Once in a while someone comes around and ask *hey, I love Xfce and would like to contribute, but where do I start? How can I be of use? How can I implement a fancy new feature?*, I have no doubt the answer is 42. Unfortunately, we don't have a supercomputer (and millions of years) to distill a meaning from that one-size-fits-all answer, therefore to offer proper guidance, some questions should be asked first, e.g. What exactly do you want to improve? Do you have any programming skills? Besides programming, how else would you like to help?
It's been a long time since I've been planning to write a comprehensive guide, I hope this to be helpful to hitchhikers and new contributors.
As any open source project, there are several ways to collaborate, everyone is welcome to help in any or many ways they are able, in this guide I'm going to explain and give hints for all contribution forms I can think of.

## Translation

Our translators do an amazing work, most of major languages are constantly updated, I really appreciate their tirelessly effort. But don't feel unmotivated, there is always room for improvement, especially if you speak any of the not so updated languages.

Xfce uses gettext which generates .po files from source code. You can view those files from any component repository, for example [Thunar](https://gitlab.xfce.org/xfce/thunar/-/tree/master/po).

Fortunately, translators don't need to know terminal commands or any complex tool, since Xfce translations are handled by [Transifex](https://www.transifex.com/xfce/public/), a web-based translation platform. At that link you can see the overview of the current status of translations.

Once you sign up, you can ask to join a translation team. Be patient, it may take a while for a coordinator to approve your request. If you think your request is taking longer than it should, say a couple weeks, please poke us via the [translation mailing list](https://mail.xfce.org/mailman/listinfo/xfce-i18n).

After joining a team, Transifex should be intuitive, there is even a comments section in case of doubts for a particular text to be translated, but developers are not notified. In this case I recommend using the mailing list or [bug tracker](https://bugzilla.xfce.org/).

For further details check the documentation [page about translations](https://docs.xfce.org/contribute/translate/start).

## Donations

If you have spare coins to donate, the official way to do so is via [Xfce's bountysource page](https://www.bountysource.com/teams/xfce). You can donate to the organization itself or put a reward of a specific bug. The money is more than welcome, but we are not actively making use, hence I hint donors to place rewards for things they expect (bug fixes, features, etc). Even if you make a hefty donation, we would be very thankful, but this is an open source project 100% run by volunteers, no one is implicitly obliged to act upon your requests.

## Bug Reporting / Testing

This one could be of your interest if you are an enthusiast eager for new features and not afraid of rough edges.
Xfce versioning is quite simple, even versions (e.g. 4.12) are stable and odd ones (e.g. 4.13) are development versions.
Since development cycles are very long (2~4 years), at some point the development version gets good enough to be used (read "tested") on a daily basis.
Unsurprisingly development version users may find regressions (new bugs) and getting reports for them is invaluable to developers, this ensures the stable release will be more solid for more people when it comes out.

The [bug tracker](https://bugzilla.xfce.org/) is where those bug reports live. Please try your best to look if a bug has already been reported and please try to be as more descriptive as possible, but avoid verbosity. Mozilla has a nice guide on [how to write a bug report](https://developer.mozilla.org/en-US/docs/Mozilla/QA/Bug_writing_guidelines).

Have some Programming/QA/DevOps knowledge? Please, please, please lend a hand to [xfce-test](https://github.com/schuellerf/xfce-test), we need automated tests really bad.

## Theming

Are you more into design and CSS is a breeze for you? Good news, gtk3 themes are completely written in CSS, you can even use a preprocessor such as Sass.
Truth must be said, since the introduction of gtk 3.0 (2011, I guess) there were several compatibility breaks, many theme authors got fed up and abandoned their projects. Fortunately things are more stable since 3.20 (I guess).

Our friends of [Project Shimmer](https://shimmerproject.org/) have been doing an amazing job, their theme Greybird is shipped on Xubuntu and is now Xfce's reference theme. Xfce is also supposed to look good under Adwaita (gtk's default theme). By the way, until 4.12 (gtk2) Xfce ships several classic themes, unfortunately they had to be [archived](https://git.xfce.org/archive/gtk-xfce-engine/tree/themes) because they need to be rewritten for gtk3.

Finally, as a theme author what are your contribution options? I would say: contribute to Greybird, port/rewrite the classic themes to gtk3, improve Xfce support in other themes out there or roll your own theme!

Since you made this far in this section, perhaps you have web design skills, if so, improvements to our website are also welcome. You may want to file reports for the [www.xfce.org](https://bugzilla.xfce.org/buglist.cgi?component=General&list_id=44458&product=www.xfce.org&resolution=---) project. Just keep in mind that Xfce's philosophy is about minimalism.

## Documentation

Our [wiki](https://wiki.xfce.org/) and [docs](https://docs.xfce.org/) sites contain many helpful pages, but one doesn't need to browse much to notice that some have outdated information.
Think you can help us with that? Please write a draft or two and share them via the [mailing list](https://mail.xfce.org/mailman/listinfo/xfce), we may then give you permissions to edit those pages.

Xfce documentation has some [hints on how to write docs](https://docs.xfce.org/contribute/documentation).

## Coding

This is the most effective way to help, we are always looking for new people to improve, fix, hack and eventually maintain Xfce's components. You don't have to be a ninja, just the basic knowledge of a programming language, preferably C, a bit of git and most importantly the desire to learn. Some people are scared of C, because they heard it's too low level... Fear not, the language is quite simple. Yes, there are pitfalls and gotchas, as any other language, but the experience is improved by gtk's and glib's utility functions and abstractions.

First things first, Xfce's modular architecture feature several [components](https://xfce.org/projects), some are part of its [core](https://gitlab.xfce.org/xfce) and some are optional [apps](https://gitlab.xfce.org/apps) or [panel plugins](https://gitlab.xfce.org/panel-plugins). Take some time to read their description. You might wonder *what the heck is a window manager?* or *I never heard of freedesktop.org or d-bus, are they edible?*. Search for them, I can't possibly explain everything there is to know about Linux desktops in a single blog post.

In my opinion the best way to get started with code is to scratch your own itch, you know, deal with that annoying bug or a behavior that could be improved. The rule of thumb is to browse [Xfce's Bugzilla](https://bugzilla.xfce.org/) and look for that bug or report it in case no one noticed the problem until now. Then go to [Xfce's gitlab](https://gitlab.xfce.org), clone the repository for the component you are about to hack, fix the problem and attach a patch to the bug report. That's easy for me to say, isn't it? I'm going to prove you it is not that hard, let's go step by step.

*Update: this section is now part of [Xfce's Wiki](https://docs.xfce.org/contribute/dev/coding/example).*

#### Building from source

Suppose we are interested in hacking xfce4-appfinder, the first thing we need to do is to build and be able to run that component:

```
git clone git://gitlab.xfce.org/xfce/xfce4-appfinder
cd xfce4-appfinder
./autogen.sh --prefix=/usr --enable-debug
make
```

The `./autogen.sh` command will fail if you never compiled a Xfce component before, we need to have installed development packages for dependencies, unfortunately it's hard to give instructions since package names vary between distributions. In most cases it helps a lot to not panic and read the error message. For example:

```
checking for exo-2 >= 0.12.0... not found
*** The required package exo-2 was not found on your system.
```

For Debian/Ubuntu `sudo apt install libexo-2-dev` does the trick. Actually on Debian/Ubuntu `sudo apt build-dep [package-name]` installs all build dependencies of the given package, `xfce4-appfinder` in our case. On Arch Linux, there is no *-dev packages, if you have Xfce installed, you will need to figure out fewer dependencies packages to install and you can also check the `makedepends` variable from the [PKGBUILD](https://git.archlinux.org/svntogit/packages.git/tree/trunk/PKGBUILD?h=packages/xfce4-appfinder) of the component you are interested.

Moving on, the `--prefix=/usr` option is useful if you want to install the component on your system (with `sudo make install`), it means to replace the version provided by the system package manager. Be aware that daily usage of development builds is cool because of unreleased fixes and new features, but it's also risky because new bugs may appear or due incompatibilities with stable components.

The `--enable-debug` allows interesting things for development such as debugging with gdb, more detailed backtraces and compiling warnings. Keep in mind that binaries with debug symbols are larger and possibly slower, often unnoticeable.

After `make`, the binary is ready to run, however xfce4-appfinder as some other Xfce components run in background (daemon mode), in this case we need to stop its process with `xfce4-appfinder -q`. Hint: this specific component has a preference to disable daemon mode (Preferences -> General -> Keep running instance in the background), so I recommend disabling it while in "write code-compile-run" loop. Now from the root of the repository, run `src/xfce4-appfinder`. Congratulations, you have just built your first component! If you don't believe me, change the window title "Application Finder" (`appfinder-window.c`) to something else, build and run again with `make && src/xfce4-appfinder`.

This was just a quick summary of how to build Xfce components, the wiki has a much more [detailed explanation](https://docs.xfce.org/xfce/building).

#### Smashing bugs

Now to make things interesting let's fix a bug, but this time I need you to clone and build [Mousepad](https://gitlab.xfce.org/apps/mousepad/), Xfce's text editor. The steps are very much the same, except that Mousepad does not run in background which makes things easier. Go on, clone and build it. Hopefully you have successfully built Mousepad by now, if not read carefully error messages spilled on the terminal, if you can't figure them out searching those messages on the web could be helpful. If you tried really hard and nothing worked, ask for guidance at #xfce-dev, stay online and be patient, try one more time if no one replies after one day.

Now you are able to execute Mousepad with `mousepad/mousepad` from the source folder, we are ready to smash a real bug. Obviously I wouldn't be so reckless to let a bug live just for beginners fix it and never push the fix, the bug I have in mind was fixed centuries ago (2014), actually it was one of my first contributed patches.
With the magic of git, we can travel back to mousepad-0.3.0 (gtk2!) and smash that bug once again. Before we go back, clean the source folder with `make distclean`, now you are good to run `git checkout mousepad-0.3.0`. Git will complain that "you are in 'detached HEAD' state", you might know what that means, otherwise ignore it for now and remember to learn git later, because you know, having a detached head is not comfortable at all ;)

Once again configure and build Mousepad (`./autogen.sh && make`) and fix the bug... Oh, but I haven't even told what is broken :) Allow me: execute Mousepad, type "hello world", save the file somewhere and close Mousepad. Now run Mousepad again and open that file, type some gibberish and choose File -> Revert, it will ask for confirmation, press "Revert" and it says it failed to revert even though it worked. Weird, isn't it?

So where do we get started? Have a look at the terminal, it says `g_error_free: assertion 'error != NULL' failed`, looks fishy. Open Mousepad source folder in your favorite editor. I hope the editor you are using features a text search on all files, because to locate the suspect part of code, we need to search for the error message from the dialog, in this case "Failed to reload the document.". Ignore `.po` files, they are used only for translations. If you are still following me this far, you might have found the message at `mousepad-window.c:3983` and look! Just below that line there is `g_error_free` which was mentioned by that terminal message, so we must be close, my dear Watson. Notice how that chunk of code is executed only if `succeed` is `FALSE`, and `succeed` is the result of `mousepad_file_reload` function call. Hmmm, let's go into that function (`mousepad-file.c:859`), take your time to read it.

As you might have reckoned (or not, no worries), it starts with state checking, checks if the file still exists, clears a buffer and, the most important part, reloads the file, the result goes into a boolean also called `succeed`. At this point, you may want to use gdb to debug this code, but I won't teach you this, there are lots of tutorials out there. The poor's man debug is `printf`, I use it a lot, though some claim it's a bad practice. Anyway, try it, put `g_print ("succeed is %s\n", result ? "TRUE" : "FALSE");` in the line after `succeed` gets assigned (`mousepad-file.c:886`), then build and try to reproduce the bug, messages on terminal may help you understand what is happening. Ok, indeed `succeed` is `FALSE` at that point, so let's dive into `mousepad_file_open`, then read it.

Found anything interesting? No? Go back and check its signature. Still no? What about its return type? Yes, it returns gint which is assigned to a gboolean variable! How is that even possible? If you know a bit C, you probably know any non-zero number yields `TRUE` when evaluated in a boolean expression, consequently `0` yields `FALSE`. If you read that function code, you saw that it returns non-zero when something went wrong (a common pattern in C programs and libraries). By now it should be clear that this is the opposite of what we expect for `succeed`, 0 means no error but when converted to boolean results in `FALSE`. So what is the fix? Well, try to figure it out yourself, you have all the information needed :)

Once you have your solution, compare it to the one provided in [Bug #10636](https://bugzilla.xfce.org/show_bug.cgi?id=10636).

#### Sharing Code

Now you know how to build components and smash bugs, browse Xfce's [bug tracker](https://bugzilla.xfce.org/describecomponents.cgi) and try to fix something that looks easy. If you have an idea on how to fix or some code that seems to work but you are not so sure, don't be afraid to ask at #xfce-dev.
Once you have a good enough solution, attach a patch (see `git commit` & `git format-patch`) to the bug report. Wait a few days, if you get no answer, poke us at #xfce-dev or use the Xfce4-dev mailing list.
After some merged patches, you may [ask commit rights](https://docs.xfce.org/contribute/dev/get-a-contributor-account) and join the dev club, yay!

By the way, (I hope that) soon we will move our infra to GitLab, so merge requests will be the new standard way to share code, much more convenient IMHO.

#### Tools

- Use whatever text editor/IDE you are comfortable with.
- The terminal is your friend, get used to it, then you will love it.
- Now that almost all components are gtk3-based, [GtkInspector](https://wiki.gnome.org/Projects/GTK+/Inspector) is an invaluable tool.
- Offline documentation browser such as [Devhelp](https://wiki.gnome.org/Apps/Devhelp) and [Zeal](https://zealdocs.org/) are faster and more convenient than using a web browser.
- [Glade](https://glade.gnome.org/) is a [WYSIWYG](https://en.wikipedia.org/wiki/WYSIWYG) interface editor, many Xfce components have their ui created with it.
- [D-Feet](https://wiki.gnome.org/Apps/DFeet) is useful when dealing with D-Bus.
- Tricky bugs will need advanced tools to find their cause, in this case [gdb](https://www.gnu.org/software/gdb/) and [valgrind](https://www.valgrind.org/) are good companions.
- Xorg's utilities, for instance `xev` and `xprop`.

#### Recommended reading

- [How to start contributing to Xfce or any other open source project](https://blog.xfce.org/2012/11/)
- Any decent book about C, there are many free books on the web (although I enjoyed Head First C).
- [The GLib/GTK+ Development Platform](https://people.gnome.org/~swilmet/glib-gtk-book/)
- [Pro Git](https://git-scm.com/book/)

## Communication

- General user questions? [Xfce's forum](https://forum.xfce.org/) and #xfce at IRC/Freenode are the best place to get help.
- Translation stuff? [Xfce-i18n](https://mail.xfce.org/mailman/listinfo/xfce-i18n) mailing list.
- Stuck with anything related to code? [Xfce4-dev](https://mail.xfce.org/mailman/listinfo/xfce4-dev) mailing list. Besides that #xfce-dev at IRC/Freenode is where devs hang out. All of us have a real life (I think) and live across different time zones, so once again, be patient and stay online.

## Conclusion

I wasn't sure where to tackle this subject, so here it is: maintainers are awesome folks, but don't take this role too seriously, it creates frustration in many ways.

Let me explain: someone is trying to figure out how to fix a bug or introduce a new feature, but may think that effort is a waste of time since the maintainer *should* be much more experienced and able to implement it in the blink of an eye. The bug is not updated for a long time so users get tired of waiting (*it's an absurd, this bug is from 2008!*), probably the maintainers are lazy, stupid or both. It doesn't take long to maintainers also get tired and abandon development for their own reasons. Finally the component is considered unmaintained which greatly reduces the chances of contributions (patches) make their way into releases.

Don't take that as a rant or as "shut up and let's work at our own pace". What I mean is that newcomers are more than welcome to propose solutions and send patches, do not expect a dedicated maintainer for the every component (people come and go). Be proactive, take part, propose, ask, learn, disagree, fix, explain, help and eventually you become a maintainer :)

That's it, I hope this guide covers as much as possible contribution forms as possible, even at the penalty of its length.
And remember, this is a volunteer-based project not a job so have fun!
