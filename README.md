Sublime Automatic CSS comments
=========================

Using automatic styleguide generation like <a href="https://github.com/darcyclarke/DSS/" title="DSS">DSS</a> or KSS is all well and good, but typing those comments is a pain!

This sublime plugin will try and figure out all that stuff for you and comment whatever CSS blocks you want. 

<h2>How?</h2>
Just type <code>///</code> followed by <kbd>tab</kbd> directly above the CSS section you want commenting and boom! Done.<br/>
It will also check the rest of your CSS/SCSS/LESS file for related states or attributes and add them as states in the comments too, plus it will give
a guess at a suggested markup.

<h2>Install</h2>
<h3>Package Manager</h3>
Press <kbd>Ctrl + Shift + P</kbd> (<kbd>Cmd + Shift + P</kbd> on OSX) and search "install"<br/>
Then Search for 'CSS comments' in the Sublime package manager and select it

<h3>Manual</h3>
Just download this repositry and dump the folder in the Sublime Packages folder

<h2>Example</h2>

Say you have some masterful CSS like this

```css
button{
  background: #006dcc;
  font-size: 18px;
  color: #eee;
  border: 1px solid rgba(0,0,0,0.5);
  border-radius: 3px;
  padding: 10px;
  box-shadow: -3px -21px 21px -9px rgba(0,0,0,0.4) inset;
}
button.active{
  background: maroon;
}

button:disabled{
  background: #aaa;
  color: #777;
}
````

Just do this

```css
///[tab]
button{
  background: #006dcc;
  font-size: 18px;
  color: #eee;
  border: 1px solid rgba(0,0,0,0.5);
  border-radius: 3px;
  padding: 10px;
  box-shadow: -3px -21px 21px -9px rgba(0,0,0,0.4) inset;
}
button.active{
  background: maroon;
}

button:disabled{
  background: #aaa;
  color: #777;
}
````

And magically!


```css
/**
  * @name Button
  * @description Style for the button element
  * @state .active - active state
  * @state :disabled - disabled state
  * @markup
  *   <button>markup</button>
  */

button{
  background: #006dcc;
  font-size: 18px;
  color: #eee;
  border: 1px solid rgba(0,0,0,0.5);
  border-radius: 3px;
  padding: 10px;
  box-shadow: -3px -21px 21px -9px rgba(0,0,0,0.4) inset;
}
button.active{
  background: maroon;
}

button:disabled{
  background: #aaa;
  color: #777;
}
````

Woo!

Now you can spend less time commenting your stylesheets and more time... writing your stylesheets.

It will also work with nested SCSS/LESS structures

```scss
/**
  * @name Button
  * @description Style for the button element
  * @state .active - active state
  * @state :disabled - disabled state
  * @markup
  *   <button>Markup</button>
  */

button{
  background: #006dcc;
  font-size: 18px;
  color: #eee;
  border: 1px solid rgba(0,0,0,0.5);
  border-radius: 3px;
  padding: 10px;
  box-shadow: -3px -21px 21px -9px rgba(0,0,0,0.4) inset;

  &.active{
    background: maroon;
  }

  &:disabled{
    background: #aaa;
    color: #777;
  }
}
````


And then run your <a href="https://github.com/darcyclarke/DSS/" title="DSS">DSS</a> builder and out pops some pretty, effortless styleguides!

e.g.
<img src="http://i.imgur.com/iNSNJsc.png" title="DSS example"/>
