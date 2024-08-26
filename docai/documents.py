from mongoengine import (
    Document,
    StringField,
    IntField,
    FloatField,
    ListField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    DateTimeField,
)
import datetime


class TimeStampedDocument(Document):
    """
    Abstract base class that adds timestamp fields to derived documents.
    Includes 'created_at' and 'updated_at' fields which are automatically set.
    """

    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField()

    meta = {"abstract": "True", "indexes": ["-created_at", "-updated_at"]}

    def save(self, *args, **kwargs):
        """
        Overridden save method to automatically update the 'updated_at' field to the current time.
        """
        self.updated_at = datetime.now()
        return super(TimeStampedDocument, self).save(*args, **kwargs)


class MetaInfo(EmbeddedDocument):
    """
    Embedded document for storing metadata about the document.
    """

    document_name = StringField(required=True)
    doc_parser_model = StringField(required=True)
    entity_extractor_model = StringField(required=True)
    total_cost = FloatField(required=True)
    total_tokens = IntField(required=True)


class ContactInfo(EmbeddedDocument):
    """
    Embedded document for storing contact information.
    """

    name = StringField(required=True)
    address = StringField(required=True)
    city = StringField(required=True)
    state = StringField()
    postal_code = StringField()
    country = StringField()
    phone = StringField()
    email = StringField()
    tax_id = StringField()


class PackageDetails(EmbeddedDocument):
    """
    Embedded document for storing package details.
    """

    description = StringField(required=True)
    quantity = IntField(required=True)
    gross_weight = StringField(required=True)
    seal_number = StringField()
    container_number = StringField()


class ParsedDocument(EmbeddedDocument):
    """
    Embedded document for storing parsed document contents.
    """

    contents = StringField(required=True)


class BillOfLading(Document):
    """
    Document schema for a Bill of Lading, including details about the shipper, consignee, vessel, ports, packages, and metadata.
    """

    task_id = StringField(unique=True, required=True)
    shipper = EmbeddedDocumentField(ContactInfo, required=True)
    consignee = EmbeddedDocumentField(ContactInfo, required=True)
    vessel = StringField(required=True)
    voyage_number = StringField(required=True)
    port_of_loading = StringField(required=True)
    port_of_discharge = StringField(required=True)
    place_of_delivery = StringField(required=True)
    packages = ListField(EmbeddedDocumentField(PackageDetails), required=True)
    issue_date = StringField(required=True)
    bl_number = StringField(required=True)
    parsed_content = StringField(required=True)
    meta_info = EmbeddedDocumentField(MetaInfo, required=True)

    meta = {"db_alias": "docai", "collection": "docai.bill_of_lading"}
