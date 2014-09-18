import sys
if sys.version_info[0] < 3:
    next = lambda x: x.next()
    bytes = str
    str = unicode

from .util import Specification, is_url, is_email


class Source(Specification):
    """
    Source object which can be added to a DataPackage object or a Resource
    object to represent where the data comes from.

    From the specification:
    Each source hash may have name, web and email fields.
    """

    SPECIFICATION = {'name': str,
                     'web': str,
                     'email': str}

    @property
    def web(self):
        """
        Link to the source of the data on the web
        """
        return self['web']

    @web.setter
    def web(self, value):
        if not value:
            if 'web' in self:
                del self['web']
            return

        if not is_url(value):
            raise ValueError("not a url: {}".format(value))

        self['web'] = value

    @property
    def email(self):
        """
        Email address to the source of the data (person, organisation etc.)
        """
        return self['email']

    @email.setter
    def email(self, value):
        if not value:
            if 'email' in self:
                del self['email']
            return

        if not is_email(value):
            raise ValueError("not an email address: {}".format(value))

        self['email'] = value


def get_sources(descriptor):
    """An array of source hashes. Each source hash may have name, web and
    email fields.

    Defaults to an empty list.

    """
    return descriptor.get('sources', [])


def set_sources(descriptor, val):
    if not val:
        val = []

    sources = []
    for source in val:
        keys = set(source.keys())
        extra_keys = keys - set(["name", "web", "email"])
        if len(extra_keys) > 0:
            raise ValueError(
                "source has unexpected keys: {}".format(extra_keys))
        if "name" not in keys:
            raise ValueError("source is missing a name")
        if "web" in keys and not is_url(source["web"]):
            raise ValueError("not a url: {}".format(source["web"]))
        if "email" in keys and not is_email(source["email"]):
            raise ValueError(
                "not an email address: {}".format(source["email"]))
        sources.append({
            str(key): str(val) for key, val in source.iteritems()})

    names = [source["name"] for source in sources]
    if len(names) != len(set(names)):
        raise ValueError("source names are not unique")

    descriptor['sources'] = sources


def add_source(descriptor, name, web=None, email=None):
    """Adds a source to the list of sources for this datapackage.

    :param string name: The human-readable name of the source.
    :param string web: A URL pointing to the source.
    :param string email: An email address for the contact of the
        source.

    """
    source = dict(name=str(name))
    if web:
        source["web"] = str(web)
    if email:
        source["email"] = str(email)

    sources = get_sources(descriptor)
    sources.append(source)
    set_sources(descriptor, sources)


def remove_source(descriptor, name):
    """Removes the source with the given name."""
    descriptor_sources = get_sources(descriptor)
    sources = [s for s in descriptor_sources if s["name"] != name]
    if len(sources) == len(descriptor_sources):
        raise KeyError("source with name '{}' does not exist".format(name))
    set_sources(descriptor, sources)
