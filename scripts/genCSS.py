'''
syntax for options:
type: 'single'|'multi',
showHeaderPic: bool,
showFooter: bool,
showFooterIcon: bool,
footerIconSrc: string,
showHeaderPic: bool,
containerBorderWidth: int,
containerBorderColor: hex,
containerBorderRadius: int (int (int int)),
containerBackground: hex,
showTweetPic: bool,
tweetBackground: hex,
-tweetBorderWidth: int,
-tweetBorderColor: hex,
-tweetBorderRadius: int (int (int int)),
tweetSideMargin: int (int),
tweetBottomMargin: int,
tweetInnerPadding: int (int (int int)),
tweetTextColor: hex,
tweetTextSize: int,
tweetTextLinkColor: hex,
tweetTextHandleColor: hex,
tweetShowTime: bool,
tweetShowVia: bool,
tweetShowActions: bool,
	(if single)
showName: bool,
showHandle: bool,
	(if multi)
headerPicSource: string,
'''
def genCSS(options):
	finalOutput = ''
	wrapperText=[]
	if options.has_key('tweetBackground'):
		wrapperText.append('background-color: #' + options['tweetBackground'])
	if options.has_key('tweetBorderWidth') and options['tweetBorderWidth'] != 0:
		if options.has_key('tweetBorderColor'):
			wrapperText.append('border: ' + str(options['tweetBorderWidth']) + 'px solid #' + options['tweetBorderColor'])
		else:
			wrapperText.append('border: ' + str(options['tweetBorderWidth']) + 'px solid #000')
	if options.has_key('tweetBorderRadius') and options['tweetBorderRadius'] != 0:
		for vendorPrefix in ['-moz-', '-webkit-', '']:
			wrapperText.append(vendorPrefix+'border-radius: ' + ' '.join([str(rad) + 'px' for rad in options['tweetBorderRadius'].split(' ')]))
	return '.tweetStream-wrapper .tweetItemWrapper {\n' + ''.join(['\t' + line + ';\n' for line in wrapperText]) + '}'
	