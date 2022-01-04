# NEA Digital Signage - Screen (client)
This project contains the code for displaying JSON responses from the digial signage server on a connected screen.  
## **Documentaton**
## Template JSON Documentation
Content is formatted as a JSON document. It follows a structure similar to that of the DOM. The document consists of an array of elements or nodes, each of which can themselves contain the same sort of array.
### **Nodes**
Nodes follow a standard format
```json
{ 
    "type": "type",
    "parameter1": "argument",
    "parameter2": "argument",
    "content": []
}
```
Every node has a `type` and a `content` parameter, and different `type` elements have unique additional parameters.
>`"type": string`  
>The type of the current element

>`"content": Array | Object | string`  
>Depending on the `type` of the node, `content` will take a different data type
>- If `content` is an Array, then it should contain a list of child nodes to the current node
>- If it is an Object, then it should contain one singular child node
>- If it is a string, then it should contain the static string content of the node

Most nodes also have `container-style` parameters.
>`"container-style': Object`  
>An Object that contains any valid CSS3 properties and their values, which is used to style the container that contains the content node
### Rows and columns
At the top level, the document is composed of `row` and `column` type nodes. An array of one of these types contains all of the respective type that exist at the current level. For example, an array of three `row` nodes means that the parent node will be divided into three separate spaces for content to be placed; this could be page content, or further `row` and `column` children.  
>`"type": "row" | "column"`

Each of thise type of node has two other parameters
>`"size": integer`  
> The relative size of the node in comaprison to the total size of all nodes at the current level

and
>`"content": Array`  

**Note: at any given level that contains `row` or `column` nodes, that level may only contain the same type of node.**  
Example
```json
{
    "type": "row",
    "size": 2,
    "content": []
}
```
### **Content nodes**
There are various types of content nodes that define the content to display on the page.
### Empty
Empty nodes are empty containers and can be used as spacers.
>`"type": "empty"`

>`"container-style": Object`  
>An Object that contains any valid CSS3 properties and their values, used to style the empty container

Empty nodes are the ony nodes that do not have `content`.  
Example
```json
{
    "type": "empty",
    "container-style": {
        "background-color": "red"
    }
}
```
### Text
Text nodes display text statically on the page.
>`"type": "text"`

>`"style": Object`  
>An Object that contains any valid CSS3 properties and their values, used to style the `<p>` HTML element that contains the text

>`"content": Object`  
>An Object that contains the source for the text to be drawn from as a [text content Object](#text-content-object)

Example
```json
{
    "type": "text",
    "style": {
        "font-family": "Arial",
        "font-size": "30px"
    },
    "container-style": { 
        "background-color": "red"
    },
    "content": {}
}
```
### Image
Image nodes display static images.
>`"type": "image"`

>`"container-style": Object`

>`"content": string`  
>A string that holds a URL from which the image can be loaded

Example
```json
{
    "type": "image",
    "container-style": { 
        "background-color": "red"
    },
    "content": "https://cdn.discordapp.com/attachments/419612262949453846/927928163495985182/tom.jpg"
}
```
### Video
Video nodes display videos that autoplay and loop.
>`"type": "video"`

>`"container-style": Object`

>`"content": string`  
>A string that holds a URL from which the video can be loaded

Example
```json
{
    "type": "video",
    "container-style": { 
        "background-color": "red"
    },
    "content": "https://www.w3schools.com/tags/movie.mp4"
}
```
### Slideshow
Slideshow nodes display a looping list of videos or images, as [slideshow content Objects](#slideshow-content-object). Videos play until they have completed, and then progress to the next slide. Images show for a pre-defined length of time.
>`"type": "slideshow"`

>`"container-style": Object`

>`"content": Array`  
>An array of [slideshow content Objects](#slideshow-content-object)

Example
```json
{
    "type": "slideshow",
    "container-style": {
        "background-color": "red"
    },
    "content": []
}
```
### Marquee
Marquee nodes display scrolling text horizontally or vertically.
>`"type": "scrolling-horizontal" | "scrolling-vertical"`

>`"style": Object`  
>An Object that contains any valid CSS3 properties and their values, used to style the `<p>` HTML element that contains the text

>`"container-style": Object`

>`"content": Array`  
>An array of [text content Objects](#text-content-object)

Example
```json
{
    "type": "scrolling-vertical",
    "style": {
        "font-family": "Arial",
        "font-size": "30px"
    },
    "container-style": {
        "background-color": "red"
    },
    "content": []
}
```
### **Content Objects**
Inside of some [content nodes](#content-nodes), content is defined by a content Object. This tells the node where it should source its content from when this type content is more complex than a string.
### Text content Object
Inside of [text](#text) and [marquee](#marqee) nodes, the content is specified as a text content Object.
- text
    >Text where the content is a static string

    >`"type": "text"`

    >`"content": string`  
    >The string of content to be displayed
- rss
    >This text pulls data from an RSS feed

    >`'type": "rss"`

    >`"format": string`  
    >A [template string](#template-string) that defines how the RSS content should be formatted. Any tags used in the template must exist on the RSS feed

    >`"length": integer`  
    >The maximum number of elements from the feed to display. A value of `-1` will use every element in the response

    >`"url": string`  
    >The URL of the RSS feed
- clock
    >A realtime clock

    >`"type": "clock"`

    >`"format": string`  
    >A [template string](#template-string) that defines how the clock should be formatted. Valid tags are
    >- `h12` - hour, 0-12
    >- `h24` - hour, 0-24
    >- `min` - minute
    >- `sec` - second
    >- `day` - day, 0-31
    >- `month` - month, 0-12
    >- `year` - year
    >- `wday` - weekday (e.g. 'Wednesday')
    >- `mname` - month name (e.g. 'July')
    >- `per` - period of day (e.g. 'PM')

Example
```json
{
    "type": "rss",
    "format": "${title} - ${description} - ",
    "length": 5,
    "url": "http://feeds.bbci.co.uk/news/rss.xml"
}
```
### Slideshow content Object
Inside of [slideshows](#slideshow), there are Arrays of slidshow content Objects.
- image
    >`"type": "image"`

    >`"time": integer`  
    >The number of milliseconds that this image should be shown for, before progressing to the next slide

    >`"content": string`  
    >A string that holds a URL from which the image can be loaded
- video
    >`"type": "video"`

    >`"content": string`  
    >A string that holds a URL from which the video can be loaded

Example
```json
{
    "type": "image",
    "time": 3000,
    "content": "https://cdn.discordapp.com/attachments/419612262949453846/927928163495985182/tom.jpg"
}
```

### **Template string**
Template strings follow a similar style to JavaScript [template literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals). They are contained in regular JSON string deliminators (`"`), rather than backticks. A string has syntax such as  
`"${<tag1>}<spacer1>${<tag2>}<spacer2>"`  
Each `${}` is replaced by the data that the tag represents. For example,  
`"${title} - ${description}"`  
when used in an [RSS feed](#text-content-object) could become  
`"Elizabeth Holmes: Theranos founder convicted of fraud - The Silicon Valley ex-CEO faces a lengthy term in prison for defrauding investors."`  
`$` characters cannot be used inside of tags or spacers.