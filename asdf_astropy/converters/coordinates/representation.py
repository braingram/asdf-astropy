from asdf.extension import Converter


class RepresentationConverter(Converter):
    tags = ("tag:astropy.org:astropy/coordinates/representation-*",)
    types = (
        "astropy.coordinates.CartesianDifferential",
        "astropy.coordinates.CartesianRepresentation",
        "astropy.coordinates.CylindricalDifferential",
        "astropy.coordinates.CylindricalRepresentation",
        "astropy.coordinates.PhysicsSphericalDifferential",
        "astropy.coordinates.PhysicsSphericalRepresentation",
        "astropy.coordinates.RadialDifferential",
        "astropy.coordinates.RadialRepresentation",
        "astropy.coordinates.SphericalCosLatDifferential",
        "astropy.coordinates.SphericalDifferential",
        "astropy.coordinates.SphericalRepresentation",
        "astropy.coordinates.UnitSphericalCosLatDifferential",
        "astropy.coordinates.UnitSphericalDifferential",
        "astropy.coordinates.UnitSphericalRepresentation",
    )

    def to_yaml_tree(self, obj, tag, ctx):
        components = {}
        for c in obj.components:
            value = getattr(obj, "_" + c, None)
            if value is not None:
                components[c] = value

        return {
            "type": type(obj).__name__,
            "components": components,
        }

    def from_yaml_tree(self, node, tag, ctx):
        from astropy.coordinates import representation

        return getattr(representation, node["type"])(**node["components"])
