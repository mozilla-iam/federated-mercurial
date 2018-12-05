# federated-mercurial


CLI application that handled federated authentication for Mercurial users

## Sequence diagram

![Sequence diagram](https://raw.githubusercontent.com/mozilla-iam/federated-mercurial/master/docs/img/sequence.png)


## Run a test hgweb

```
$ make docker-build
$ make docker-run
```

By default it will listen on http://localhost:8000, with the port exposed, a default test repo and no SSL (DO NOT USE
THIS FOR ANYTHING ELSE THAN LOCAL TESTING)


### Test HTTP pushes

```
$ hg clone http://localhost:8000/test
$ cd test
$ touch test
$ hg add test
$ hg commit test
$ hg push http://localhost:8000/test
pushing to http://localhost:8000/test
searching for changes
remote: adding changesets
remote: adding manifests
remote: adding file changes
remote: added 1 changesets with 1 changes to 1 files
```
