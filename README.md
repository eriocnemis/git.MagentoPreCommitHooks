# Magento Pre-Commit Hooks
Magento Pre-Commit Hooks are used for identifying simple issues before submission to code review, they can also fix some problems automatically. These are made as plugin for the [pre-commit hooks framework](https://pre-commit.com/).

### Using with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/eriocnemis/git.MagentoPreCommitHooks
    rev: 1.0.1  # Use the ref you want to point at
    hooks:
    -   id: magento-phpcs
        args: ["php=php7.4", "--autofix=true"]
    # -   id: ...
```

### Hooks available

#### `magento-phpcs`
PHP CodeSniffer is able to fix many errors and warnings automatically.
You can configure this with the following commandline options:
  - `--php=php7.4` - Alias or full path to the executable file of PHP. Defaults php.
  - `--autofix=true` - Automatically fixes encountered violations as possible. Defaults false.
  - `--standard=Magento2` - The name or path of the coding standard to use. Defaults Magento2.

#### `magento-phpstan`
PHPStan is a static analysis system for PHP projects. It finds bugs in your codebase by inspecting the source files.
You can configure this with the following commandline options:
  - `--php=php7.4` - Alias or full path to the executable file of PHP. Defaults php.
  - `--level=1` - Specifies the rule level to run. Defaults max.
  - `--autoload-file=dev/tests/api-functional/framework/autoload.php` - Specifies the path to a custom autoloader.
  - `--configuration=dev/tests/phpstan.neon` - Specifies the path to a configuration file.
