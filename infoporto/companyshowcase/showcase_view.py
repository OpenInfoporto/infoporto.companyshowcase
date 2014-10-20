from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ShowcaseView(BrowserView):

    template = ViewPageTemplateFile('companies_list_templates/view.pt')

    def __call__(self):
        """"""
        self.hello_name = getattr(self.context, 'hello_name', 'World')
        return self.template()
