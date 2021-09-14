# Magento Pre-Commit Hooks
Magento Pre-Commit Hooks are used for identifying simple issues before submission to code review, they can also fix some problems automatically. These are made as plugin for the [pre-commit hooks framework](https://pre-commit.com/).

## Usage

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/eriocnemis/git.MagentoPreCommitHooks
    rev: 1.0.8  # Use the ref you want to point at
    hooks:
    -   id: magento-phpcs
        args: ["php=php7.4", "--autofix"]
    -   id: magento-phpmd
    # -   id: ...
```

### Hooks available

#### `magento-phpcs`
PHP Code Sniffer provides the mechanism of checking code compliance with specific coding standard.
You can configure this with the following commandline options:
  - `--php=php7.4` - Alias or full path to the executable file of PHP. Defaults php.
  - `--autofix` - Automatically fixes encountered violations as possible.
  - `--standard=Magento2` - The name or path of the coding standard to use. Defaults Magento2.

#### `magento-phpmd`
PHP Mess Detector provides a diverse set of pre defined rules to detect code smells and possible errors within the analyzed source code.
You can configure this with the following commandline options:
  - `--php=php7.4` - Alias or full path to the executable file of PHP. Defaults php.
  - `--rule-sets=codesize,cleancode` - Set of rules which will be applied against the source under test. Defaults codesize,cleancode,design.

#### `magento-phpstan`
PHP Static Analysis Tool finds bugs in your codebase by inspecting the source files.
You can configure this with the following commandline options:
  - `--php=php7.4` - Alias or full path to the executable file of PHP. Defaults php.
  - `--level=1` - Specifies the rule level to run. Defaults max.
  - `--autoload-file=dev/tests/api-functional/framework/autoload.php` - Specifies the path to a custom autoloader.
  - `--configuration=dev/tests/phpstan.neon` - Specifies the path to a configuration file.

#### `magento-phpcpd`
PHP Copy Paste Detector finds duplicate code in PHP files.
You can configure this with the following commandline options:
  - `--php=php7.4` - Alias or full path to the executable file of PHP. Defaults php.
  - `--min-lines=12` - Specify a minimum number of identical lines. Defaults 5.

#### `magento-phpunit`
Automatically run PHPUnit tests.
You can configure this with the following commandline options:
  - `--php=php7.4` - Alias or full path to the executable file of PHP. Defaults php.
  - `-c=dev/tests/unit/phpunit.xml` - Specifies the path to a configuration file.

#### `magento-webapi-rest-phpunit`
Automatically run REST API PHPUnit tests.
You can configure this with the following commandline options:
  - `--php=php7.4` - Alias or full path to the executable file of PHP. Defaults php.
  - `-c=dev/tests/api-functional/phpunit_rest.xml` - Specifies the path to a configuration file.

#### `magento-webapi-soap-phpunit`
Automatically run SOAP API PHPUnit tests.
You can configure this with the following commandline options:
  - `--php=php7.4` - Alias or full path to the executable file of PHP. Defaults php.
  - `-c=dev/tests/api-functional/phpunit_soap.xml` - Specifies the path to a configuration file.

## License

All Free Eriocnemis extensions is distributed under the [Open Software License (OSL 3.0)](https://github.com/eriocnemis/git.MagentoPreCommitHooks/blob/master/LICENSE.md), and is thus open source software.

## Contribution

Want to contribute to this extension? The best possibility to provide any code is to open a [pull requests](https://github.com/eriocnemis/git.MagentoPreCommitHooks/pulls) on GitHub. Please, see the [CONTRIBUTING.md](https://github.com/eriocnemis/git.MagentoPreCommitHooks/blob/master/.github/CONTRIBUTING.md) file for more.

## Suggestions

We're also interested in your feedback for the future of our extension. You can submit a suggestion or feature request through the [issue](https://github.com/eriocnemis/git.MagentoPreCommitHooks/issues) tracker. But you must acknowledge and agree that your offer will not prevent Eriocnemis team from using your ideas without obligation to you. General decision will depend on the specific proposal.

## Support

If you encounter any problems or bugs, please open a [issue](https://github.com/eriocnemis/git.MagentoPreCommitHooks/issues). To make this process more effective, we're asking that these include more information to help define them more clearly. Pleace, do not enumerate multiple bugs or feature requests in the same issue. Similarly do not add your issue as a comment to an existing issue. Many issues look similar, but have different causes.

Also note that the issue tracker is not a support forum. If you have questions about how to use the extension, or how to get extension to work, please visit stackoverflow.com.

<p align="center"><img src="https://avatars3.githubusercontent.com/u/48807026?s=48&v=4"></p>
