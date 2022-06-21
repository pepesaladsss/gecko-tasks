# Gecko Tasks

Gecko Tasks is a simple-to-use program designed to make it significantly easier to get started making programs to crawl or debug websites. It uses Selenium with geckodriver to simulate user behavior, with the optional ability to use a list of proxies for Requesters to use. You can scale it up to as many Requesters as you want using the Tasks.json file which includes all of Gecko Tasks’ configuration options.

Gecko Tasks is **not** a lightweight program by nature. It runs actual browser instances (Completely separate from your own, using a standalone executable of Firefox's geckodriver), not *just* web requests. This means that per requester, you could be looking at about 300mb of RAM usage, which you’ll need to consider as you scale up.


## Installation

For installing/setting up Gecko Tasks, you'll need to install [Python **3.10**+](https://www.python.org/downloads/), run `pip install selenium`, and download [geckodriver](https://github.com/mozilla/geckodriver/releases) from Mozilla's GitHub, then drag the executable into Gecko Tasks' folder. 

After doing all of that, you'll likely want to check out `Tasks.json` and change the options there to your liking. Run `python RequestHandler.py` to run Gecko Tasks after creating your own Task Flow, or to run the example that Gecko Tasks comes shipped with to make sure everything is working as intended.
## Creating Tasks

### `ERROR_FINISH and SUCCESS_FINISH` - Don’t use as Task Names.

**Do not use these keywords as Task names!**

There are some keywords for navigating the task flow which allow you to handle errors and successful requests in a straightforward way. Here’s all the available options:

**`NEXT`** is useful for simply continuing to the next Task

**`PREVIOUS`** is useful if you need to repeat some actions in the event of an error

**`REFRESH_PROXY`** allows you to grab a new Proxy if a page failed to load or didn’t load some elements (some proxies may block requests to certain sites or assets)

**`FIRST`** allows you to completely restart the task flow if you want to loop the requests or need to start over.

**You can also use a Task’s name as a keyword!!**

If you have a Task named `EXAMPLE_DELAY_TASK`, you can use it as the value for `SUCCESS_FINISH` or `ERROR_FINISH` to direct the Requesters to that Task if needed.

### `GET` - Goes to a URL defined within the Task.

Requesters will go to the defined **`URL`** when running this task. If there’s an error loading the page or connecting, the function (or keyword function) at `ERROR_FINISH` will be run. Otherwise, `SUCCESS_FINISH` will run if nothing went wrong. 

```json
"GET_EXAMPLE": {
    "TYPE": "GET",
    "URL": "https://www.example.com",
    "SUCCESS_FINISH": "NEXT",
    "ERROR_FINISH": "NEXT"
},
```

### `DELAY` **- Delays the Requesters for a set amount of seconds**

Requesters will wait for an amount of time defined in `VALUE` (in seconds)

 

```json
"DELAY_EXAMPLE": {
    "TYPE": "DELAY",
    "VALUE": 5,
    "SUCCESS_FINISH": "NEXT",
    "ERROR_FINISH": "NEXT"
},
```

### **`FIND`** - Finds an Element

A barebones way to find an element, useful for knowing when a page’s content is fully loaded or not, but doesn’t feature any ways to get that element’s information or interact with it.

```json
"FIND_EXAMPLE": {
    "TYPE": "FIND",
    "BY": "See Below",
    "VALUE": "See Below",
    "SUCCESS_FINISH": "NEXT",
    "ERROR_FINISH": "NEXT"
},
```

**`BY`** - You can use these values:

- `XPATH`
- `ID`
- `CSS_SELECTOR`

### **`FIND_AND_CLICK`** - Finds an element and clicks it

A complete copy of **`FIND`** with a click sent after the element is found.

```json
"FIND_EXAMPLE": {
    "TYPE": "FIND",
    "BY": "See Below",
    "VALUE": "See Below",
    "SUCCESS_FINISH": "NEXT",
    "ERROR_FINISH": "NEXT"
},
```

**`BY`** - You can use these values:

- `XPATH`
- `ID`
- `CSS_SELECTOR`

`VALUE` - Put the element’s XPATH, ID, or CSS_SELECTOR, depending on what you’ve set `BY` to. 

### **`FIND_WITH_FRAME`** - Find an element contained within a frame (Not Recommended)

It’s recommended that you use **`SELECT_FRAME`** and then use **`FIND`** instead of this so you know where an issue lies in your task flow if you need to debug things.

```json
"FIND_WITH_FRAME_EXAMPLE": {
    "TYPE": "FIND_WITH_FRAME",
    "FRAME_BY": "XPATH",
    "FRAME_VALUE": "FrameXPATH",
    "BY": "ID",
    "VALUE": "ElementID",
    "SUCCESS_FINISH": "NEXT",
    "ERROR_FINISH": "NEXT"
}
```

**`FRAME_BY & BY`** - You can use these values:

- `XPATH`
- `ID`
- `CSS_SELECTOR`

It’s recommended you use `XPATH` with IFrames, they’re often created with randomized IDs and so only the “Full XPATH” (Right click and copy in DevTools) will work to reference the IFrame consistently.

`FRAME_VALUE/VALUE` - Put the element/frame’s XPATH, ID, or CSS_SELECTOR, depending on what you’ve set `FRAME_BY/BY` to. 

### **`SELECT_FRAME`** - Selects an IFrame to access elements contained within it

Some elements may be contained within an IFrame, if this is the case, you’ll need to select it prior to accessing those elements. 

```json
"SELECT_FRAME_EXAMPLE": {
    "TYPE": "SELECT_FRAME",
    "BY": "See Below",
    "VALUE": "See Below",
    "SUCCESS_FINISH": "NEXT",
    "ERROR_FINISH": "NEXT"
},
```

**`BY`** - You can use these values:

- `XPATH`
- `ID`
- `CSS_SELECTOR`

It’s recommended you use `XPATH`, though, because a lot of IFrames are created with randomized IDs and so only the “Full XPATH” (Right click and copy in DevTools) will work to reference the IFrame consistently.

`VALUE` - Put the element’s XPATH, ID, or CSS_SELECTOR, depending on what you’ve set `BY` to. 

### **`FIND_ELEMENT_OUTPUT_TO_VAR`** - Find an element, make it a variable

Finds an element, then stores it as a variable on each Requester that runs the Task. It’s able to be repeatedly referenced as long as the code is running, and can be used to get information from its attributes. These variables are stored separately for each Requester.

```json
"FIND_ELEMENT_OUTPUT_TO_VAR_EXAMPLE": {
    "TYPE": "FIND_ELEMENT_OUTPUT_TO_VAR",
    "BY": "ID",
    "VALUE": "ElementID",
    "VARIABLE_NAME": "ExampleName",
    "SUCCESS_FINISH": "NEXT",
    "ERROR_FINISH": "NEXT"
},
```

**`BY`** - You can use these values:

- `XPATH`
- `ID`
- `CSS_SELECTOR`

**`VALUE`** - Put the element’s XPATH, ID, or CSS_SELECTOR, depending on what you’ve set `BY` to. 

**`VARIABLE_NAME`** Can be referenced with other Tasks. You can use variables in `URL` tasks by putting a **`$`** at the start of the `URL` value.

### **`GET_ELEMENT_ATTRIBUTE`** - Get the value of a stored element’s attribute

If you use **`FIND_ELEMENT_OUTPUT_TO_VAR`**, you may want to access that element’s attributes such as `src` or `value`. Using this Task type, you can specify an element (stored as a variable), an attribute, and an output variable’s name which you can access in some other tasks.

```json
"ELEMENT_ATTRIBUTE": {
    "TYPE": "GET_ELEMENT_ATTRIBUTE",
    "INPUT_VARIABLE_NAME": "ElementVariable",
    "ATTRIBUTE": "src",
    "OUTPUT_VARIABLE_NAME": "OutputVariable",
    "SUCCESS_FINISH": "NEXT",
    "ERROR_FINISH": "NEXT"
}
```

**`ATTRIBUTE`** - Any valid HTML attribute that the element has will be usable here, if it doesn’t have the attribute, the task will error out.

**`OUTPUT_VARIABLE_NAME`** - This variable name can be referenced in URLs if you put **`$`** at the start of the URL string (Within the quotes), and other task types if specified.

### **`APPEND_VARIABLE_TO_FILE`** - Append a variable’s data to a specified file

If you have a variable created by another task, you can append the variable’s data to a file using this task type.

```json
"APPEND_VARIABLE_TO_FILE_EXAMPLE": {
    "TYPE": "APPEND_VARIABLE_TO_FILE",
    "INPUT_VARIABLE_NAME": "Example_Variable",
    "NEWLINE": "TRUE",
    "OUTPUT_FILE_NAME": "Example.txt",
    "SUCCESS_FINISH": "NEXT",
    "ERROR_FINISH": "NEXT"
}
```

**`INPUT_VARIABLE_NAME`** - The name of a variable created by another task.

**`NEWLINE`** `(TRUE/FALSE)` - Creates a new line at the *end* of the variable’s data, useful for repeatedly printing content to a file.

**`OUTPUT_FILE_NAME`** - The name of the file you want to output to.
