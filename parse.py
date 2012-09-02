import re
import lxml.html
import lxml.etree


html=open("jcorebiz","r").read()

l = lxml.html.fromstring(html)

for item in l.xpath('//table[@id="proLayout"]'):
	props = dict()
	props['img'], = item.xpath('tr/td[@class="jacket"]/img/@src')
	rawProps = dict()
	for propName in item.xpath('tr/th/text()'):
		if propName == 'sound':
			continue
		raw = ''.join(item.xpath('tr/th[text()="%s"]/following-sibling::td[1]/text()' % (propName,)))
		if propName == 'price':
			match = re.match("([0-9,]+)YEN", raw)
			real = int(re.sub(",", "", match.group(1)))
		elif propName in ('cutNo', 'media', 'label', 'artist', 'title', 'description'):
			real = raw
		else:
			raise Exception("Unknown property: %s" % (propName,))
		props[propName] = real
	print "%s:%s" % (props["cutNo"], ",".join([ "%s=%s" % (name, re.sub("\r", "", re.sub("\n", "\\\\n", re.sub("([,\\\\])", "\\\\\\1", unicode(value))))) for (name, value) in props.items() if name != 'cutNo' and value ]))
