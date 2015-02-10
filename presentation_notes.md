before -

1. Chrome - github project repo, docker hub, fig, boot2docker, circle-ci
1. Terminal - make sure boot2docker is up, make sure fitter-happier-docker is up (with no virtualenv activated, on the master branch)

### Fitter. Happier. More Productive.

- play radiohead song
- Alright, so we have a lot of material to cover today so let's dive right in.

---

## About Me

- Full-stack web developer
- Co-founder/Author of [Real Python](https://realpython.com)
- For all you Javascript fans, I just started teaching at Node bootcamp. Let's just say - I'm excited for ES6.

---

## Real Python

- So just a little about Real Python - our focus is on experiential learning. Building fun projects with the goal of learning the Python syntax, web development basics, and the web frameworks Flask and Django.
- And yes - we have a coupon code for you!

---

## Today

So, the focus today is to detail a practical workflow that you can take with you to incorprate in your own projects.

- Honestly, I struggled a bit with how best to present this material. It's a lot, and - frankly - many of the solutions out there either don't work as well as advertised or their docs are terrible. I did a lot of hacking to find some answers.
- We're covering a lot of material today. Don't worry if you miss something or don't fully understand a concept since this entire workflow will be featured in a blog post on Real Python - https://realpython.com. The post will go live on 02/10/2015.
- I recommend just watching me go through the workflow, and then recreate it on your own next week when the post goes live.
- If you have questions, I recommend saving them until the end since we have a lot to cover. Also, I have delivered this same workflow to a few meetup groups and I've found that people generally get their questions answered at a later time in the tutorial.

---

## What is Docker?

- With Docker you can easily deploy a web application along with the app's dependencies, environment variables, and configuration settings: everything you need to recreate your environment quickly and efficiently.
- There are a few terms that you need to be aware of:
    - A *Dockerfile* is a file that contains a set of instructions used to create an *image*.
    - An *image* is used to build and save snapshots (the state) of an environment.
    - A *container* is an instantiated, live *image* that runs a collection of processes.
- These are the big three. As long as you remember the relationship between the three then you'll be fine.

---

## Why Docker?

- You can truly mimic your production environment on your local machine. No more having to debug environment specific bugs or worrying that your app will perfrom differently in production (in theory, at least).

---

## Workflow!

The workflow is fairly straightforward:

1. Code locally on a feature branch
1. Open a pull request on Github against the master branch
1. Run automated tests against the Docker container
1. If the tests pass, manually merge the pull request into master
1. Once merged, the automated tests run again
1. If the second round of tests pass, a build is created on Docker Hub
1. Once the build is created, it's then automatically (err, automagically) deployed to production

---

# Part 1 - Local Setup

Let's start with getting our local dev environment set up.

---

## Docker Setup

And this begins with Docker, of course.

- Mac and Windows users need Boot2Docker in order to power Docker containers since Docker requires certain features from the Linux kernel in order to properly run.
- Before you download Boot2Docker, grab the project boilerplate from Github. I've set up three tags that can be used as you go through the tutorial. For time's sake, I'm going to use my local version.
- Create and activate a virtualenv.
- Now you would want to download and install boot2docker.
- Once installed, test it out - `boot2docker version`

---

## Fig Up!

- Fig handles the building and running of multiple services. It makes it super easy to link services together running in different containers. Fig is actually being replaced. Well, not so much replaced. More of a name change. To Docker Compose. This will probably happen in the next month or so.
- You can install fig with pip. Just follow the instructions on the fig.sh website. Or just install the requirements from the repo, which conatins fig as a dependency. `pip install -r requirements.txt`. This will take just a second.
- Once installed, test it out - `fig --version`
- Now let's look at the fig config file.
- First, we build the image from the "web" directory and then mount that directory to the "code" directory within the Docker container. The Flask app is ran via the `python app.py` command. This exposes port 5000 on the container, which is forwarded to port 80 on the host environment.
- Next, the Redis service is built from the Docker Hub "Redis" image. Then port 6379 is exposed and fowarded.
- All very straightforward. There is an underline Dockerfile in the web directory, but for time's sake, I'll let you look at the blog post for details on how that's working.

---

## Build and Run

- The `fig up` command builds an image for our Flask app, pulls the Redis image, and then starts everything up in seperate containers.
- This will take some time to build the first time you run it. After that, each line in your Docker file is cached - so subsequent runs will go much quicker. If you do change a line in your code, it will recreate everything in that line - so be mindful of this when you structure your Dockerfile. More on this in the blog post.
- Now we can view our app in the browser by navigating to the address associated with the boot2docker VM - `boot2docker ip`.

---

# Part 2 - Continuous Integration

At this point we've set up our local environent. Next, let's add CI into the mix.

---

## Docker Hub

- Docker Hub is like Github, only for Docker images.
- As for the CI part, I configure Docker Hub to only build new images when code is update on Github. Docker Hub then pulls in the updates and recreates the image. I like this approach since it is one last line of defense before pushing to staging or production.
- There are some drawbacks to this - namely that you can't push updated images directly to Docker Hub. Docker Hub must pull in changes and create the images itself to ensure that their are no errors. Keep this in mind as you go through this workflow. The Docker documentation is not clear with regard to this matter.
- So, before Docker Hub builds a new image, we should use a *true* CI server to catch errors.

---

## CircleCI

And that's exactly where CircleCi comes into play.

- Given a Dockerfile, CircleCI builds an image, starts a new container, and then runs tests inside that container.
- Setup si simple: Sign up with your Github account, then add the Github repo to create a new project. This will automatically add a webhook to the repo so that anytime you push to Github a new build is triggered.
- You also need a config file so that CircleCi knows how to create the build.
- Essentially, we create a new image, run the container, then run the unit tests.
- The deployment section relies on an env variable that contains a simple Curl command to issue a POST request to Docker Hub once the tests pass on the master branch.

---

## Feature Branch Workflow

So, with all the services setup let's go through a typical development process.

- And, yes: I did skip some necessary config to truly link the process together. You can get all that from the highly detailed blog post.
- In short: You need to configure Docker Hub to only create a new build after Circle CI runs the tests on the master branch - and they are successful.
- Create a new branch: `git checkout -b pytn-test master`
- Let's add a simple assert - `self.assertNotEqual(four, 7)`
- Commit, then puhs - `git push origin pytn-test`
- Create the PR.
- If you hop over to CircleCi, you can see the build running based on the intructions from the config file.
- One thing I love about CircleCI is the excellent documentation. They also have great support. And no - they are not paying me to say that. They are an excellent tool for CI. Check them out even if you are not using Docker.
- Okay. So once the tests pass, let's manually merge the PR in Github. This will tigger a new build.
- As that build runs, let's talk a bit about the options you have after they pass.
- Remember how I said that I configured Docker Hub to pull updated code to create a newimage? Well, you could also set it up to where you can push images directly to it. So once these test pass, you could simply push the image to update Docker Hub and then deploy to staging or production. Since I have it set up differently, I handle the push to production from Docker Hub, not CircleCI. There's positives and negatives to both approaches. The decision is your's.
- Once the second round of tests pass, this will trigger a new build on Docker Hub via the Curl command that I spoke about a few minutes ago. Again, this is all detailed in the blog post.
- And you can see that building on Docker Hub.

---


## Conclusion

- Well, my hope was to show delivery as well, but we just don't have time. We went over a lot. Take a breath. Or two.
- In the blog post, my app is housed on Digital Ocean, and I set up a different Flask app that handles a POST request sent from Docker Hub when a new image finishes building. This app then checks to ensure that the key associated with the POST request is correct and then it stops creates a new container and stops the old one. It's not exactly zero-dowtime. More like as minimal downtime as possible. That said, the app can be tweaked to eliminate downtime.
- There are plenty of services out there that handle delivery as well, including CircleCI. They are far from perfect and most suggest that you do not utilize them for production apps.
- That's all I have. I'd love to hear from you, especially if you have a different workflow that works for you Either add some comments to the blog post or email me directly. Thank you.

