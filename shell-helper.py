#!/usr/bin/python
# Shell script document generator.
import sys, os, json, csv

def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def find_files(first_file):
  to_process = list()
  with open(first_file, 'r') as openfile:
    for line in openfile:
      if line.startswith("source "):
        file = os.path.expandvars(line[len("source "):]).rstrip()
        to_process += find_files(file)
  to_process.append(first_file)
  return to_process

def find_shell_helpers_in_file(f):
    printables = list()
    building_function = False
    building_helper = False
    comment_lines = list()
    documentation_name = ""
    with open(f, 'r') as openfile:
      for line in openfile:
        # Track comments for use with helpers
        if line.startswith("#") and not line.startswith("#?") and not line.startswith("#!"):
          comment_lines.append(line[len("#"):].strip())
        else:
          if line.lower().startswith("#!"):
            echo = line[len("#!"):].rstrip()
            printables.append(EchoDocumentation(echo))
          if line.lower().startswith("#?"):
            documentation_name = '$ ' + line[len("#?"):].strip()
          elif line.lower().startswith("function "):
            documentation_name = line[len("function "):].split("(")[0].split("{")[0].strip()
          elif line.lower().startswith("alias "):
            alias = line[len("alias "):].split("=")
            documentation_name = alias[0].strip()
            comment_lines.append("... " + alias[1].strip())

          function_ready = len(comment_lines) > 0 and documentation_name
          # Finalize your docs
          if function_ready:
            printables.append(RunnableFunction(documentation_name, comment_lines))
          if not line.startswith("#") or function_ready:
            # Reset built object
            comment_lines = list()
            documentation_name = ""
            building_function = False
            building_helper = False
      return ShellScript(f, printables)

def find_shell_helpers(filenames):
  outputs = list()
  for f in filenames:
    outputs.append(find_shell_helpers_in_file(f))
  first_col_width = max(shell_script.len() for shell_script in outputs) + 2

  for shell_script in outputs:
    shell_script.printo(first_col_width)

class ShellScript:

  def __init__(self, filename, printables):
    self.filename = filename
    self.printables = printables

  def printo(self, first_col_width):
    print(self.filename)
    row_boolean = True
    for printable in self.printables:
      printable.printo(first_col_width, row_boolean)
      row_boolean = not row_boolean
    print("")

  def len(self):
    if len(self.printables) is 0:
        return 0
    return max(printable.len() for printable in self.printables)

class RunnableFunction:

  def __init__(self, name, comment_lines):
    self.name = name
    self.comment_lines = comment_lines

  def len(self):
    return len(self.name)

  def printo(self, first_col_width, row_boolean):
    row_start = "" if row_boolean else "\033[90m"
    row_end = "" if row_boolean else "\033[0m"
    print row_start + "  " + self.name.ljust(first_col_width) + "# " + ", ".join(self.comment_lines).ljust(first_col_width) + row_end

class EchoDocumentation:

  def __init__(self, echo):
    self.echo = echo

  def len(self):
    return 0

  def printo(self, first_col_width, row_boolean):
    print self.echo

if __name__ == "__main__":
  first_file_path = os.path.abspath(sys.argv[1])
  print("Scanning functions in: " + first_file_path)
  files_targeted = unique(find_files(first_file_path))
  print("")
  find_shell_helpers(files_targeted)