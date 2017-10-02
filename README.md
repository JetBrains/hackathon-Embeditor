[![JetBrains team project](http://jb.gg/badges/team-plastic.svg)](https://confluence.jetbrains.com/display/ALL/JetBrains+on+GitHub)

Embeditor
=========

The idea behind the project is that many users like code completion and
inspections provided by IntelliJ, but they prefer Vim or Emacs as programmer's
text editors. The only current solution is using Vim emulation in IntelliJ
provided by IdeaVim plugin.

We would like to see more options here:

* Using code completion and inspections from a running instance of IntelliJ in
  a separate Vim process. The main benefit of this approach is native Vim
  experience enhanced by powerful code insight of IntelliJ.

* Embed Vim as a terminal editor in IntelliJ IDE instead of the regular editor
  and provide code completion and inspections there. The point here is
  combination of the full Vim editor with plugins, scripts,
  etc. and the nearly complete set of IntelliJ features: code navigation,
  run configurations and others.

* Run Vim locally and connect to a headless IntelliJ instance on a remote host.
  This would enable, for example, rich code editing in vim over SSH.


Features
--------

* Vim editor embedded into IntelliJ via terminal emulator
* IntelliJ based completion and resolve support

To-do List
----------

* (done) Terminal window in IntelliJ instead of the editor that runs Vim
* (done) IntelliJ-based completion and resolve for embedded Vim
* (done) IntelliJ-based completion and resolve invoked from real Vim (vim plugin)
* Vim plugin that highlights code based on a list of errors/warnings from IntelliJ
* Synchronization of saved file contents between Vim and IntelliJ
* (done) Synchronization of edited file contents between Vim and IntelliJ

Problems
--------

* Terminal emulator needs to be improved
* Handle the case of opening file in vim after incorrect termination
* Soft-wrap in Vim prevents to map lines in buffer to file lines easyliy


Demo
----

The current state of the plugin looks like that:

![Embeditor](https://github.com/JetBrains/hackathon-Embeditor/raw/master/embeditor/doc/embeditor.png)

Here you can see vim terminal session opened instead of normal IDEA editor with the IDEA completion popup.


Authors
-------

* traff
* zolotov
* vlan
