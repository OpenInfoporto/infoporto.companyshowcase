from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Item

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder


from infoporto.companyshowcase import MessageFactory as _

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import xmlrpclib

# Interface class; used to define content-type schema.

class ICompanySearch(form.Schema, IImageScaleTraversable):
    """
    Description of the Example Type
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/company_search.xml to define the content type.

    form.model("models/company_search.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class CompanySearch(Item):
    grok.implements(ICompanySearch)

    # Add your class methods and properties here
    pass


# View class
# The view will automatically use a similarly named template in
# company_search_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    """ sample view class """

    grok.context(ICompanySearch)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
    def getSections(self):
        openerp = Openerp()
        args = [] 
        fields = ['id', 'name'] 

        data = openerp.getItems(args, fields, 'membership.section')

        sections = []
        for d in data:
            sections.append(dict(id=d['id'], name=d['name']))

        return sections


class Openerp():

    def __init__(self):
        self.username = 'admin' #the user
        self.pwd = 'c0nf1ndustr1@'      #the password of the user
        self.dbname = 'openconfindustria'    #the database

        # Get the uid
        sock_common = xmlrpclib.ServerProxy ('http://open.confindustriasp.it/xmlrpc/common')
        self.uid = sock_common.login(self.dbname, self.username, self.pwd)

        #replace localhost with the address of the server
        self.sock = xmlrpclib.ServerProxy('http://open.confindustriasp.it/xmlrpc/object')

    def getItems(self, args, fields, model):
        ids = self.sock.execute(self.dbname, self.uid, self.pwd, model, 'search', args)
        data = self.sock.execute(self.dbname, self.uid, self.pwd, model, 'read', ids, fields)

        return data

    def getAddress(self, partner_id):
        args = [('partner_id', '=', partner_id), ('type', 'ilike', 'delivery')]
        fields = ['name', 'address', 'phone', 'fax', 'type', 'street2', 'city', 'country', 'street', 'email']
        ids = self.sock.execute(self.dbname, self.uid, self.pwd, 'res.partner.address', 'search', args)
        data = self.sock.execute(self.dbname, self.uid, self.pwd, 'res.partner.address', 'read', ids, fields)

        return data


class doSearch(BrowserView):
    template = ViewPageTemplateFile('company_search_templates/search.pt')

    def getItems(self):
        #TODO: name
        openerp = Openerp()
        args = [('membership_section_id', '=', int(self.request.section)), ('name', 'ilike', self.request.name)]
        fields = ['id', 'name']
        data = openerp.getItems(args, fields, 'res.partner')
        return data
        
    def __call__(self):
        return self.template()

class companyDetails(BrowserView):
    template = ViewPageTemplateFile('company_search_templates/details.pt')

    def getItems(self):
        openerp = Openerp()
        args = [('id', '=', int(self.request.id))]
        fields = ['id', 'name', 'website', 'merceologia']
        partner = openerp.getItems(args, fields, 'res.partner')
        address = openerp.getAddress(int(self.request.id))
        return [dict(partner=partner[0], address=address[0])]

    def __call__(self):
        return self.template()

