Run 

```
docker build -t travis_cli .
```

to intall Travis CLI as per https://github.com/travis-ci/travis.rb#installation .

Run 

```
docker run -it --rm -v $(PWD):/git_repo travis_cli bash
```

to start the CLI.
