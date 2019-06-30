# Code Climate Cppcheck Engine

`codeclimate-cppcheck` is a Code Climate engine that wraps [Cppcheck][cppcheck].
You can run it on your command line using the Code Climate CLI, or on our
hosted analysis platform.

[Cppcheck][cppcheck] is a static analysis tool for C/C++ code.

## Installation

1. If you haven't already, [install the Code Climate CLI][codeclimate-cli].
2. [optional] Run `codeclimate engines:install cppcheck` to install the Code
   Climate Cppcheck engine.
3. Configure your `.codeclimate.yml` file. See example below.
4. You're ready to analyze! Browse into your project's folder and run
   `codeclimate analyze`. If you skipped step 2, the Cppcheck engine will
   automatically be installed at this point, assuming it's enabled in
   `.codeclimate.yml`.

## Configuration

Like the `cppcheck` command line tool itself, you can configure various
aspects of the static analysis. Right now, the following options are supported
in `.codeclimate.yml`:

* `check`: issue categories to check. Available values are: `all`, `warning`,
  `style`, `performance`, `portability`, `information`, `unusedFunction`, etc.
  Refer to the `--enable=` option of `cppcheck` for more information.
* `project`: use Visual Studio project/solution (`*.vcxproj`/`*sln`) or compile
  database (`compile_commands.json`) for files to analyse, include paths,
  defines, platform and undefines.
  Refer to the `--project=` option of `cppcheck` for more information.
* `language`: forces `cppcheck` to check all files as the given language.
  Valid values are: `c`, `c++`.
  Refer to the `--language=` option of `cppcheck` for more information.
* `stds`: multiple language standards to check against.
  Refer to the `--std=` option of `cppcheck` for more information.
* `platform`: specifies platform specific types and sizes. Available builtin
  platforms are: `unix32`, `unix64`, `win32A`, `win32W`, `win64`, etc.
  Refer to the `--platform=` option of `cppcheck` for more information.
* `defines`: define preprocessor symbols.
  Refer to the `-D` option of `cppcheck` for more information.
* `undefines`: undefine preprocessor symbols.
  Refer to the `-U` option of `cppcheck` for more information.
* `includes`: paths for searching include files. First given path is searched
  for contained header files first. If paths are relative to source files,
  this is not needed.
  Refer to the `-I` option of `cppcheck` for more information.
* `max_configs`: maximum number of configurations to check in a file before
  skipping it. Default is '12'.
  Refer to the `--max-configs=` option of `cppcheck` for more information.
* `inconclusive`: allow reporting issues that are not inconclusive.
  Refer to the `--inconclusive` option of `cppcheck` for more information.

Additional options may be supported later.

An example `.codeclimate.yml` file:

```yaml
version: 2
plugins:
  cppcheck:
    enabled: true
    config:
      check: all
      project: compile_commands.json
      language: c++
      stds:
        - c++11
      platform: unix64
      defines:
      - "DEBUG=1"
      - "__cplusplus"
      undefines:
      - "DEBUG"
      includes:
      - include/
      max_configs: 42
      inconclusive: false
```

## Need help?

For help with [Cppcheck][cppcheck], check out their documentation.

If you're running into a Code Climate issue, first look over this project's
GitHub Issues, as your question may have already been covered.
If not, [go ahead and open a support ticket with us][codeclimate-help].

[cppcheck]: http://cppcheck.sourceforge.net/
[codeclimate-cli]: https://github.com/codeclimate/codeclimate
[codeclimate-help]: https://codeclimate.com/help
