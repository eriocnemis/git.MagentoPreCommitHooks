# Magento Pre-Commit Hooks
Magento Pre-Commit Hooks are used for identifying simple issues before submission to code review, they can also fix some problems automatically. These are made as plugin for the [pre-commit hooks framework](https://pre-commit.com/).

### Using with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/eriocnemis/git.magento_pre_commit_hooks
    rev: 1.0.1  # Use the ref you want to point at
    hooks:
    -   id: magento-phpcs
    # -   id: ...
```

### Hooks available
