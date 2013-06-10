Sublime Automatic CSS comments
=========================

Using automatic styleguide generation like DSS or KSS is all well and good, but typing those comments is a pain!

This sublime plugin will try and figure out all that stuff for you and comment whatever CSS blocks you want.

<h2>How?</h2>
Just type <code>///</code> followed by <kbd>tab</kbd> directly above the CSS section you want commenting and boom! Done.<br/>
It will also check the rest of your CSS file for related states or attributes and add them as states in the comments too

<h3>Example</h3>

Say you have some masterful CSS like this

<pre>
button{
  background: red;
}

button.active{
	background: green;
}

button:disabled{
	background: grey;
}
</pre>

Just do this

<pre>
///[tab]
button{
  background: red;
}

button.active{
  background: green;
}

button:disabled{
	background: grey;
}
</pre>

And magically!

<pre>

/**
  * @name Button
  * @description Style for the button element
  * @state .active - active state
  * @state :disabled - disabled state;
  * @markup
  *   &lt;button&gt;markup&lt;/button&gt;
  */

button{
  background: red;
}

button.active{
  background: green;
}

button:disabled{
	background: grey;
}
</pre>

Woo!

Now you can spend less time commenting your stylesheets and more time... writing your stylesheets.
