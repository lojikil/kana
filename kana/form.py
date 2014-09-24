import cgi


class FormField(object):
    __slots__ = ['name', 'autocomplete', 'type', 'value',
                 'css_class', 'description', 'error',
                 'has_errors', 'required', 'css_id',
                 'options', 'size', 'disabled']

    def __init__(self, name, **kwargs):
        self.name = name
        self.type = kwargs.get("type")
        self.value = kwargs.get("value")
        self.css_class = kwargs.get("css_class")
        self.css_id = kwargs.get("css_id")
        self.description = kwargs.get("description")
        self.required = kwargs.get("required", False)
        self.autocomplete = kwargs.get("autocomplete", False)
        self.disabled = kwargs.get("disabled", False)
        self.error = None
        self.has_errors = False
        self.options = kwargs.get("options")
        self.size = kwargs.get("size")

    def validate(self):
        if self.required and (self.value is None or self.value == ""):
            self.has_errors = True
            self.error = "Field is required"
            return False
        return True

    def label(self):
        res = []
        lbl_txt = "<label for=\"{0}\">".format(self.name)
        res.append(lbl_txt)
        if self.description:
            res.append(cgi.escape(self.description))
        else:
            tmp = self.name.title()
            res.append(' '.join(tmp.split('_')))

        if self.has_errors:
            res.append("<span class=\"error\">")
            res.append("{0}</span>".format(self.error))

        res.append("</label>\n")
        return ''.join(res)

    def render(self):
        res = []
        if not self.name:
            raise Exception("Field must have name attribute")

        res.append("<input name=\"{0}\" ".format(self.name))

        if self.type:
            res.append("type=\"{0}\" ".format(self.type))

        if self.value:
            if type(self.value) is str:
                res.append("value=\"{0}\" ".format(cgi.escape(self.value)))
            else:
                res.append("value=\"{0}\" ".format(cgi.escape(str(self.value))))

        if self.autocomplete:
            res.append("autocomplete=\"false\" ")

        if self.disabled:
            res.append("disabled ")

        if self.css_class:
            res.append("class=\"{0}\" ".format(self.css_class))

        if self.css_id:
            res.append("id=\"{0}\" ".format(self.css_id))

        res.append("/>")

        return ''.join(res)

    def __str__(self):
        return self.label() + self.render()


class IntegerFormField(FormField):

    def validate(self):
        if not super(IntegerFormField, self).validate():
            return False
        if type(self.value) is int:
            pass
        elif type(self.value) is str and self.value.isdigit():
            self.value = int(self.value)
        else:
            self.has_errors = True
            self.error = "Value is *must* be an integer"
            return False
        return True


class SelectFormField(FormField):

    def validate(self):
        if not super(SelectFormField, self).validate():
            return False

        for item in self.options:
            if self.value == str(item[0]):
                return True

        self.has_errors = True
        self.error = "Value not within supported range"
        return False

    def render(self):
        res = []

        res.append("<select name=\"{0}\" ".format(self.name))

        if self.autocomplete:
            res.append("autocomplete=\"false\" ")

        if self.disabled:
            res.append("disabled ")

        if self.css_class:
            res.append("class=\"{0}\" ".format(self.css_class))

        if self.css_id:
            res.append("id=\"{0}\" ".format(self.css_id))

        res.append(">\n")

        for item in self.options:
            res.append("<option ")
            if self.value is not None:
                if str(item[0]) == str(self.value):
                    res.append(" selected=\"selected\" ")
            res.append("value=\"{0}\">".format(item[0]))
            res.append("{0}</option>\n".format(item[1]))

        res.append("</select>\n")

        return ''.join(res)


class TextFormField(FormField):

    def render(self, **kwargs):
        res = []
        res.append("<textarea name=\"{0}\" ".format(self.name))

        if self.autocomplete or 'autocomplete' in kwargs:
            res.append("autocomplete=\"false\" ")

        if self.disabled or 'disabled' in kwargs:
            res.append("disabled ")

        if self.css_class:
            res.append("class=\"{0}\" ".format(self.css_class))

        if 'css_class' in kwargs:
            res.append("class=\"{0}\" ".format(kwargs.get('css_class')))

        if self.css_id:
            res.append("id=\"{0}\" ".format(self.css_id))

        if 'css_id' in kwargs:
            res.append("id=\"{0}\" ".format(kwargs.get('css_id')))

        if self.options is not None and 'rows' in self.options:
            res.append("rows=\"{0}\" ".format(self.options['rows']))

        if 'rows' in kwargs:
            res.append("rows=\"{0}\" ".format(kwargs.get('rows')))

        if self.options is not None and 'cols' in self.options:
            res.append("cols=\"{0}\" ".format(self.options['cols']))

        if 'cols' in kwargs:
            res.append("cols=\"{0}\" ".format(kwargs.get('cols')))

        res.append(">\n")

        if self.value:
            res.append(cgi.escape(self.value))

        res.append("</textarea>\n")

        return ''.join(res)


class WebForm(object):

    def __init__(self, data=None):
        if data is not None:
            items = self.__class__.__dict__.iteritems()
            for item in items:
                k, v = item
                if isinstance(v, FormField):
                    v.value = data.get(v.name)

    def validate(self):
        res = True
        ret = True
        items = self.__class__.__dict__.iteritems()
        for item in items:
            k, v = item
            if isinstance(v, FormField):
                res = v.validate()
                if not res:
                    ret = False
        return ret
