Java, Docker and Memory (The 3 Musketeers?)
===========================================

# Intro

Who am I? Gregory Arendse, Technical Lead at Entelect.

I am currently working on a project with Standard Bank where we are modernizing the payment space.

I have worked on projects at; Satrix, Barloworld and Discovery.

Today I want to talk about Java Docker and memory; The Three Musketeers. But we cannot talk about memory without
including CPU usage, the fourth Musketeer.

What impact does resources have on your application and how to measure the impact. I also want to show a couple tools
that can assist you.

???

# What

Let's talk about resources. How much memory does your application need? How many CPU's does your application need?

These values are easy to guess, and more often than not we will overestimate this value and not too much more thought
into it.

Traditionally Java applications would run on some kind of application server (Tomcat, WebSphere, JBoss, Wildfly), or in
some cases a Virtual Machine.

The traditional monolith, you would give the application a decent amount or resources and Java with the JVM would use
all those resources as best as it can. It does this, and it does this well.

It is becoming more common for Java applications to be deployed in the cloud using various types of Kubernetes
environments. This in combination with the raise of microservices means that over estimating how much your application
needs to run adds up quickly.

In both these cases knowing your application's resource requirements allows you to better use the resources you have
available to you.

# Why

Too much, too little, just right!

Having the right amount of resources is key, but how do we know what is right?

Firstly we have to define what we will measure; what is important? In most cases we are talking about response times,
but essentially it comes down to how long does it take for a task to complete. APIs are simple, HTTP requests typically
need to be sub-one second. In the case of batch jobs, or something similar we would still need to define what is
acceptable. This would typically be our max duration; you have a batch job that starts at 1 AM and needs to be completed
by 2 AM.

Now that we know what we are measuring, what impact does changing resources have? And how do we find "just right"?

# How

If you have an application is already being monitored, that is a good place to start, have a look at what it is
currently using. If not we will start by creating a baseline.

Run the application with no restrictions and measure what it uses.

I have written a simple API which I will use as an example today; Musketeers. Its provides a simple REST interface to
database running on Postgres. I have included a couple mappers and populated the database to create a bit of load, to
make it feel more like a real world API.

Before we can start out application and see what it uses, we need a test. Something that will place a load on the
application. The load should represent what the application will encounter in a real world environment.

The Musketeers application has basic REST endpoints; create, update, delete, get and get all. So to test my application
I need to hit each of these endpoints. Lets assume the average user requests all musketeers (get all), then creates a
new musketeer (create), gets this musketeer (get one), decides to change some detail (update) and finally removes the
musketeer (delete).

Using this, I have created a test, a load test using Apache JMeter. Other options include Gatling, Locust and many
others. Pick one that works for you.

[Demo setting up the test plan]

This is the test plan I'll be using against each variation of running the application. The idea here is, it doesn't
matter how we run the application the end user should not be affected.

To create our baseline I'm going to run the application locally with no resource constraints (other than that of what my
laptop has). I want to measure what resources the application uses. To do this I'm going to use Visual VM. Visual VM has
a nice plug-in that will allow me to measure the start-up usage.

[Demo application with Visual VM start up plug in]

??? Talk about Results

This baseline is what we will use to compare each of our runs going forward. We want to see what impact changing our
resources has on the application; not necessarily how fast the application is.

From here I want to find what our memory limit is. I want to reduce the amount of memory available to the application
and see what happens.

The JVM is very good at using the resources it has available to it. The JVM will very quickly use up more memory to
avoid having to run the garbage collector too often. ???

? Limiting memory usage using -Xmx
? Limit memory using docker

Reduce memory until application fails to start up

Compare results

Memory constraint found

Time to look at the CPU.

CPU is a bit more difficult to limit
? docker CPU limit

find minimum

? talk about thrashing

Compare results

??? Spring Native

---

Deploying a Java application to a PRD environment means knowing what kind of resources it needs to run, but how do you
know that a head of time?

Sure, its easy to give an application more hardware, but if with the rise of Kubernetes more Java applications are being
deployed in Docker containers. Most Kubernetes environments want to know what resources the Java application needs to
assist with schedulling and balancing the load accross nodes.

Further more having the wrong values mean Horizontal Pod Autoscalers scale up your pod too soon, or your pod takes too
long to start up.

I would like to work through the following

- Using a Java memory profiler we can see how much memory a Java application uses.
- See what happens when we contrain the memory using Docker and docker-compose.
- Limit the CPU using docker-compose and show what happens when the Java application does not have enough CPU
- Find a balance; not too much, not too little
- Have a look at Spring Native and GraalVM

# Why?

Too little resources is easy, applicaiton is slow or unsreponsive. A typical API response time is sub one
