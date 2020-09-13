/**
 * @license Copyright (c) 2003-2020, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */


CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here.
	// For complete reference see:
	// https://ckeditor.com/docs/ckeditor4/latest/api/CKEDITOR_config.html

	// The toolbar groups arrangement, optimized for two toolbar rows.
	config.toolbarGroups = [
		{ name: 'clipboard',   groups: [ 'clipboard' ] },
		{ name: 'editing',     groups: [ 'find', 'selection' ] },
		{ name: 'links',       groups: [ 'Links'] },
		{ name: 'insert' },
		{ name: 'forms' },
		{ name: 'others' },
		{ name: 'basicstyles', groups: [ 'basicstyles' ] },
		{ name: 'colors' },
		{ name: 'paragraph',   groups: [ 'blocks' ] },
		{ name: 'tools' },
		'/',
		{ name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
		{ name: 'styles' },
		{ name: 'about' },
		{ name: 'youtube' },
		{ name: 'clipboard',   groups: [ 'undo' ] }
	];

	config.height = 500;
	
	// Remove some buttons provided by the standard plugins, which are
	// not needed in the Standard(s) toolbar.
	config.removeButtons = 'Underline,Subscript,Superscript,Anchor,Source,Paste,PasteText,PasteFromWord,Spellchecker,Cleanup';
	// Google Web Fonts config
	config.extraPlugins = 'Youtube,ckeditor-gwf-plugin';
	config.font_names = 'GoogleWebFonts;' + config.font_names;

	// Set the most common block elements.
	config.format_tags = 'p;h1;h2;h3;pre';

	//Whether to escape basic HTML entities in the document, including:
		//&nbsp;
		//&gt;
		//&lt;
		//&amp;
	config.basicEntities = false;

	// Simplify the dialog windows.
	config.removeDialogTabs = 'image:advanced;link:advanced';
};
