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


# Interface class; used to define content-type schema.

class Icompany(form.Schema, IImageScaleTraversable):
    """
    Description of the Example Type
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/company.xml to define the content type.

    # form.model("models/company.xml")
    title = schema.TextLine(
            title=_(u"Ragione sociale"),
        )

    description = schema.Text(
            title=_(u"Breve descrizione"),
        )

    profile = RichText(
            title=_(u"Company Profile"),
            required=False
        )

    logo = NamedImage(
            title=_(u"Logo"),
            required=False,
        )

    abstract = NamedFile(
            title = _(u"Documento di presentazione"),
            description=_(u"Carica un documento riassuntivo della tua azienda")
        )

    address = schema.Text(
            title=_(u"Indirizzo")
        )

    phone = schema.TextLine(
            title=_(u"Telefono")
        )

    fax = schema.TextLine(
            title=_(u"FAX")
        )

    email = schema.TextLine(
            title=_(u"E-mail")
        )

    twitter = schema.TextLine(
            title=_(u"Twitter"),
            description=_(u"Permetti agli utenti di seguirti su Twitter")
        )

    vat = schema.TextLine(
            title=_(u"Partita IVA")
        )

    section = schema.TextLine(
            title=_(u"Sezione")
        )

    merceology = schema.TextLine(
            title=_(u"Merceologia")
        )

    slogan = schema.TextLine(
            title=_(u"Slogan")
        )

    activities = schema.Text(
            title=_(u"Attivita'")
        )

    proposition = RichText(
            title=_(u"Proposte"),
            description=_(u"Offerte speciali, promozioni limitate, ecc."),
            required=False
        )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class company(Item):
    grok.implements(Icompany)

    # Add your class methods and properties here
    pass


# View class
# The view will automatically use a similarly named template in
# company_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    """ sample view class """

    grok.context(Icompany)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here

