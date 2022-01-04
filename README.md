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
    ...
    "content": [ ... ]
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
    "content": [ ... ]
}
```
### **Content nodes**
There are various types of content nodes that define the content to display on the page.
### Empty
Empty nodes are empty containers and can be used as spacers.
>`"type": "empty"`

>`"container-style": Object`  
> An Object that contains any valid CSS3 properties and their values, used to style the empty container

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
>An Object that contains the source for the text to be drawn from

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
    "content": { ... }
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
