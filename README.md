# imagecount

Imagecount is a times visited display and a simple analytics device. It has the familiar look of sheids.io, but is written in Python. Here is an example:

![badge](http://imagecount.pythonanywhere.com/img?id=pSS_jCZ_S7JvgYZyuJjZyw)

There are some options to configure your badge too.

You can configure colors with any html/svg color or use the named colors which are listed [here](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/named-color).
The default color is teal, but here is how you make it bright red.

```md
![badge](https://imagecount.pythonanywhere.com/img?id=pSS_jCZ_S7JvgYZyuJjZyw&color=bright_red)
```

![badge](http://imagecount.pythonanywhere.com/img?id=pSS_jCZ_S7JvgYZyuJjZyw&color=bright_red&prev=true)


Also available obtions are `style` and `prev`. The available styles are (so far) "default" and "gitlab-scoped" which looks like this:

![badge](http://imagecount.pythonanywhere.com/img?id=pSS_jCZ_S7JvgYZyuJjZyw&style=gitlab-scoped&prev=true)

`prev` allows you to see what a badge looks like without affecting its count or if you want to fetch an image multiple times on a page.

Also availible are graphs. To view a graph, exchange the img in the url with graph.

![graph](https://imagecount.pythonanywhere.com/graph?id=pSS_jCZ_S7JvgYZyuJjZyw)

## Credits

This project is made with Flask, Flask-Limiter, anybadge and uses the tools made by astral.
