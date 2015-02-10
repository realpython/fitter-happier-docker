# Docker in Action - fitter, happier, more productive

Last [time](add link) we set up our local environment, detailing the basic process of building an *image* from a *Dockerfile* and then creating an instance of the *image* called a *container*. We tied everything together with fig to build and connect different containers for our Flask app as well as the Postgres and Redis processes.

**This time, let's look at a nice continuous integration workflow powered by [CircleCI](https://circleci.com/)**.

## Docker Hub

Thus far we've worked with Dockerfiles, images, and containers (abstracted by fig, of course).

Are you familiar with the Git workflow? Images are like Git repositories while containers are similar to a cloned repository. Sticking with that metaphor, [Docker Hub](https://hub.docker.com/), which is repository of Docker images, is akin to Github.

1. Signup [here](https://hub.docker.com/account/signup/), using your Github credentials.
1. Then add a new automated build. And add your Github repo that you created and pushed to in the first tutorial. Just accept all the default options, except for the "Dockerfile Location" - change this to "/web".

Once added, this will trigger an initial build. Make sure the build is successful.

### Docker Hub for CI

Docker Hub, in itself, acts as a continuous integration server since you can configure it to create a build every time you push a new commit to Github. In other words, it ensures you do not cause a regression that completely breaks the build process when the code base is updated.

> Keep in mind by using an [automated build](https://docs.docker.com/userguide/dockerrepos/#automated-builds), you cannot use the `docker push` command. Builds must be triggered by committing code to your GitHub or BitBucket repository.

Let's test this out. Add an assert to the test suite:

```python
self.assertNotEqual(four, 5)
```

Commit and push to Github to generate a new build on Docker Hub. Success?

Bottom-line: It's good to know that if a commit does cause a regression that Docker Hub will catch it, but since this is the last line of defense before deploying you ideally want to catch any breaks before generating a new build on Docker Hub. Plus, you also want to run your unit and integration tests from a *true* continuous integration server - which is exactly where CircleCI comes into play.

## CircleCI

[CircleCI](https://circleci.com/) is a continuous integration and delivery platform that supports testing within Docker containers. Given a Dockerfile, CircleCI builds an image, starts a new container, and then runs tests inside that container.

Remember the workflow we want?

1. Code locally on a feature branch
1. Open a pull request on Github against the master branch
1. Run automated tests against the Docker container
1. If the tests pass, manually merge the pull request into master
1. Once merged, the automated tests run again
1. If the second round of tests pass, a build is created on Docker Hub
1. Once the build is created, it's then automatically (err, automagically) deployed to production

Let's take a look at how to achieve just that...

### Setup

The best place to start is the excellent [Getting started with CircleCI](https://circleci.com/docs/getting-started) guide. Sign up with your Github account, then add the Github repo to create a new project. This will automatically add a webhook to the repo so that anytime you push to Github a new build is triggered. You should receive an email about this.

Next we need to add a configuration file to the root folder of repo so that CircleCI can properly create the build.

### *circle.yml*

Add the following build commands/steps:

```yaml
machine:
  services:
    - docker

dependencies:
  override:
    - pip install -r requirements.txt

test:
  override:
    - fig run -d --no-deps web
    - python web/tests.py
```


Essentially, we create a new image, run the container, then test - first that the web process is running (the app is live) and then that our unit tests pass.

> Notice how we're using the command `fig run -d --no-deps web`, to run the web process, instead of `fig up`. This is because CircleCI already has both Redis and Postgres running and available to us. So, we just need to run the web process.

With the *circle.yml* file created, push the changes to Github to trigger a new build. *Remember: this will also trigger a new build on Docker Hub.*

Success?

Before moving on, we need to change our workflow since we won't be pushing directly to the master branch anymore.

### Feature Branch Workflow

> For these unfamiliar with the Feature Branch workflow, check out [this](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow) excellent introduction.

Let's run through a quick example...

### Create the feature branch

```sh
$ git checkout -b circle-test master
Switched to a new branch 'circle-test'
```

### Update the app

Add a new assert in *tests.py*:

```python
self.assertNotEqual(four, 6)
```

### Issue a Pull Request

```sh
$ git add web/tests.py
$ git commit -m "circle-test"
$ git push origin circle-test
```

Even before you create the actual pull request, CircleCI starts creating the build. Go ahead and create the pull request, then once the tests pass on CircleCI, press the Merge button. Once merged, the build is triggered on Docker Hub.

### Refactoring the workflow

If you jump back to the overall workflow at the top of this post, you'll see that we don't actually want to trigger a new build on Docker Hub until the tests pass against the master branch. So, let's make some quick changes to the workflow:

1. Open your repository on Docker Hub, and then under *Settings* click *Automated Build*.
1. Uncheck the Active box: "When active we will build when new pushes occur".
1. Save.
1. Click *Build Triggers* under *Settings*
1. Change the status to on.
1. Copy the example curl command - i.e., `$ curl --data "build=true" -X POST https://registry.hub.docker.com/u/mjhea0/fitter-happier-docker/trigger/84957124-2b85-410d-b602-b48193853b66/`

Now add the following code to the bottom of your *circle.yml* file:

```yaml
deployment:
  hub:
    branch: master
    commands:
      - $DEPLOY
```

Here we fire the `$DEPLOY` variable *after* we merge to master *and* the tests pass. We'll add the actual value of this variable as an environment variable on CircleCI:

1. Open up the *Project Settings*, and click *Environment variables*.
1. Add a new variable with the name "DEPLOY" and paste the example curl command (that you copied) from Docker Hub as the value.

Now let's test.

```sh
$ git add circle.yml
$ git commit -m "circle-test"
$ git push origin circle-test
```

Open a new pull request, and then once the tests pass on Circle CI, merge to master. Another build is trigged. Then once the tests pass again, a new build will be triggered on Docker Hub via the curl command. Nice.

## Conclusion and Next Steps

Next time we'll look at deliverying this app to the production environment.
