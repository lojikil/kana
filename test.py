from kana.form import WebForm, IntegerFormField, FormField

# really need to convert this to an test runner instance...

class FooForm(WebForm):
    name = FormField(name="name", required=True)
    idx = IntegerFormField(name="idx", required=True)

f = FooForm(data={'name':'Stefan', 'idx': 10})
g = FooForm()
print "Original Name: ", g['name'].value
print "Original Name: ", f['name'].value
print "Original idx: ", g['idx'].value
print "Original idx: ", f['idx'].value
g['name'].value = 'Bob'
g['idx'].value = 11
print "Modified idx: ", g['idx'].value
print "Modified idx: ", f['idx'].value
