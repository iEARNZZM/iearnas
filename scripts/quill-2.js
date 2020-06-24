// Specify Quill fonts
var fontList = ['Arial', 'Courier', 'Garamond', 'Tahoma', 'Times New Roman', 'Verdana'];
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

// Configure Quill editor options
var toolbarOptions = [
    [{ 'font': fonts.whitelist }],
    ['bold', 'italic', 'underline'],
    ['clean'] 
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
        placeholder: 'Arba rašai, arba eik pas Kocienę ir paverk',
        readOnly: false,
        theme: 'snow'
    });
});

// Generate code-friendly font names
function getFontName(font) {
    return font.toLowerCase().replace(/\s/g, "-");
}