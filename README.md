# Code Climate Cppcheck Engine

`codeclimate-cppcheck` is a Code Climate engine that wraps [Cppcheck][cppcheck].
You can run it on your command line using the Code Climate CLI, or on our
hosted analysis platform.

[Cppcheck][cppcheck] is a static analysis tool for C/C++ code.

## Installation

1. If you haven't already, [install the Code Climate CLI][codeclimate-cli].
2. Run `codeclimate engines:enable cppcheck`. This command both installs the
   engine and enables it in your `.codeclimate.yml` file.
3. You're ready to analyze! Browse into your project's folder and run
   `codeclimate analyze`.

## Configuration

Like the `cppcheck` command line tool itself, you can configure various
aspects of the static analysis. Right now, the following options are supported
in `.codeclimate.yml`:

* `check`: issue categories to check. Refer to the `--enable=` option of
  `cppcheck` for available arguments.
* `exclude_paths`: multiple paths to exclude from checking. Refer to the
  `-i` option of `cppcheck`.
* `inconclusive`: allow reporting issues that are not inconclusive. Refer to
  the `-inconclusive` option of `cppcheck`.
* `stds`: multiple language standards to check against. Refer to the`--std=`
  option of `cppcheck` for available arguments.

Additional options may be supported later.

## Need help?

For help with [Cppcheck][cppcheck], check out their documentation.

If you're running into a Code Climate issue, first look over this project's
GitHub Issues, as your question may have already been covered.
If not, [go ahead and open a support ticket with us][codeclimate-help].

[cppcheck]: http://cppcheck.sourceforge.net/
[codeclimate-cli]: https://github.com/codeclimate/codeclimate
[codeclimate-help]: https://codeclimate.com/help
