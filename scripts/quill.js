// Specify Quill fonts
var fontList = ['Segoe UI', 'Arial', 'Courier', 'Garamond', 'Tahoma', 'Times New Roman', 'Verdana'];
var fontNames = fontList.map(font => getFontName(font));
var fonts = Quill.import('attributors/class/font');
fonts.whitelist = fontNames;
Quill.register(fonts, true);

// Add fonts to CSS style
var fontStyles = "";
fontList.forEach(function(font) {
    var fontName = getFontName(font);
    fontStyles += ".ql-snow .ql-picker.ql-font .ql-picker-label[data-value=" + fontName + "]::before, .ql-snow .ql-picker.ql-font .ql-picker-item[data-value=" + fontName + "]::before {" +
        "content: '" + font + "';" +
        "font-family: '" + font + "', sans-serif;" +
        "}" +
        ".ql-font-" + fontName + "{" +
        " font-family: '" + font + "', sans-serif;" +
        "}";
});

var toolbarOptions = [
    ['bold', 'italic', 'underline'],        // toggled buttons
    ['blockquote', 'code-block'],
  
    [{ 'header': 1 }, { 'header': 2 }],               // custom button values
    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
    [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
    [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
  
    [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
  
    [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
    [{ 'font': fonts.whitelist }],
    [{ 'align': [] }],

    ['link', 'image', 'video'],
  
    ['clean']                                         // remove formatting button
  ];


var quill;
$(function() {
    // Append the CSS stylesheet to the page
    var node = document.createElement('style');
    node.innerHTML = fontStyles;
    document.body.appendChild(node);

    quill = new Quill('#editor', {
        modules: {
          toolbar: toolbarOptions
        },
        placeholder: 'Kur bėga Šešupė, kur Nemunas teka...',
        readOnly: false,
        theme: 'snow'
    });
});

// Generate code-friendly font names
function getFontName(font) {
    return font.toLowerCase().replace(/\s/g, "-");
}

$('#saveDelta').click(function () {
    window.delta = quill.getContents(); // Išsaugoja visus teksto duomenis į window.delta

    quill.setContents(window.delta);    // Perrašai Editoriaus dežutę į window.delta

    console.log(window.delta);

});


$(document).ready(function(){
    $('.ql-container').height($('.ql-container').innerHeight() - $('.ql-toolbar').innerHeight() -50);
});
