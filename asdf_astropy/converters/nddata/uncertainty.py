class UncertaintyBaseConverter(Converter):
    tags = ("tag:astropy.org:astropy/nddata/uncertainty-*",)
    types = (
        "astropy.nddata.nduncertainty.StdDevUncertainty",
        "astropy.nddata.nduncertainty.UnknownUncertainty",
        "astropy.nddata.nduncertainty.VarianceUncertainty",
    )

    def from_yaml_tree(self, node, tag, ctx):
        import astropy.nddata

        return getattr(astropy.nddata, node["class"])(node["array"], node.get("unit"))

    def to_yaml_tree(self, nddata_uncertainty, tag, ctx):
        node = {}

        node["class"] = nddata_uncertainty.__class__.__name__
        node["array"] = nddata_uncertainty.array
        if nddata_uncertainty.unit is not None:
            node["unit"] = nddata_uncertainty.unit

        return node
