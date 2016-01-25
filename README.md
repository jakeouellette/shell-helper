# shell-helper
If you're like me, you're always forgetting your cute aliased utility methods you've been writing. Shell-helper solves that problem.

Shell helper shows all shell functions and aliases with documentation

# setup

Copy shell-helper.py and sh_best to your ~/ folder. Add to your .bashrc the following lines: (you could also put it in your .zshrc, or .bash_profile, but if you do, update the shell-help function.)

    source $HOME/sh_best

    # List shell functions
    function shell-help {
      python ~/shell-helper.py ~/.bashrc
    }

then, open up a new terminal and run shell-help

# Example run
python ~/dev/scripts/shell-helper.py sh_best

    Scanning functions in: /Users/jouellette/dev/projects/shell-helper/sh_best

    /Users/jouellette/dev/projects/shell-helper/sh_best

    many of these commands came from:
      http://www.commandlinefu.com/commands/browse/sort-by-votes
      http://unix.stackexchange.com/questions/6/what-are-your-favorite-command-line-features-or-tricks

      tweet                                   # Send a tweet, $1 = username, $2 = message (must be quoted)
      extract                                 # Use the proper extract command for the given file type, $1 = filename
      $ sudo !!                               # Run last command as root
      start-server-here                       # Start a simple http server in python in this directory, ... 'python -m SimpleHTTPServer'
      $ ^foo^bar                              # Run last command but replacing foo with bar
      $ !!:gs/foo/bar                         # Runs previous command replacing foo by bar every time that foo appears
      $ ctrl-x e                              # Invoke editor here
      $ <space>command                        # Invoke command without saving history
      $ 'ALT+.' or '<ESC> .'                  # Place the argument of the most recent command on the shell
      $ reset                                 # Salvage a borked terminal
      nice-mount                              # Currently mounted file systems in a nice layout, ... 'mount | column -t'
      $ echo "ls -l" | at midnight            # Execute a command at a given time
      local-access                            # start a tunnel from some machine's port 80 to your local post 2001, $1 = remote
      get-ip                                  # Get your external IP address, ... 'curl ifconfig.me'
      query-wikipedia                         # Query Wikipedia via console over DNS, $1 = wikipedia query
      output-microphone                       # output your microphone to a remote computer's speaker, $1 = remote
      $ sshfs name@server:/fldr/pth /mnt/pth  # Mount folder/filesystem through SSH

# Formatting 101

To get a command to appear in shell-help, add a comment above it. So:

    # comment
    function funcname() {
      ...
    }

will show up as:

    funcname         # comment

With aliases, the alias command will also be output. So:

    # comment
    alias aliasname='ls -l'

Will show up as:

    aliasname         # comment, 'ls -l'

If you've got a command you run a lot, but don't want to alias it, just add a function document using `#?` syntax. So:

    # Don't forget to ls -l sometimes!
    #? ls -l

Will show up as:

    $ ls -l         # Don't forget to ls -l sometimes!,

Finally, if you want to output something (e.g., a header to a section of function), use:

    #! Put anything here, hello world!
    
And it will show up in the shell helper where you added the comment, e.g.,

    Put anything here, hello world!

# Recursive sourcing

Shell helper will attempt to recursively source all sourced shells. This lets you organize your scripts, e.g., by topic. For example, you might split your shell scripts into `.backend_sh`, `.frontend_sh`, then source them from your bashrc.

# sh_best

I included in this repo a shell script with popular shell commands that serve as examples to show how to use this utility. I use a different set of commands that are mostly work-related, but I wanted to give a realistic example. :)
