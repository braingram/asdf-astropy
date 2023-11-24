import warnings

from asdf.extension import Converter


class UnitConverter(Converter):
    tags = (
        "tag:stsci.edu:asdf/unit/unit-*",
        "tag:astropy.org:astropy/units/unit-*",
    )
    types = (
        "astropy.units.CompositeUnit",
        "astropy.units.IrreducibleUnit",
        "astropy.units.NamedUnit",
        "astropy.units.PrefixUnit",
        "astropy.units.Unit",
        "astropy.units.UnitBase",
        "astropy.units.UnrecognizedUnit",
        "astropy.units.function.mixin.IrreducibleFunctionUnit",
        "astropy.units.function.mixin.RegularFunctionUnit",
    )

    def select_tag(self, obj, tags, ctx):
        from astropy.units import UnitsError, UnitsWarning

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UnitsWarning)

            try:
                obj.to_string(format="vounit")
            except (UnitsError, ValueError):
                return next(t for t in tags if "astropy.org" in t)

            return next(t for t in tags if "stsci.edu" in t)

    def to_yaml_tree(self, obj, tag, ctx):
        if "stsci.edu" in tag:
            return obj.to_string(format="vounit")

        return obj.to_string()

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.units import Unit

        kwargs = {"parse_strict": "silent"}
        if "stsci.edu" in tag:
            kwargs["format"] = "vounit"

        return Unit(node, **kwargs)
