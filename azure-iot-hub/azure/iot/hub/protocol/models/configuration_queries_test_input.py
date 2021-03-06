# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ConfigurationQueriesTestInput(Model):
    """ConfigurationQueriesTestInput.

    :param target_condition:
    :type target_condition: str
    :param custom_metric_queries:
    :type custom_metric_queries: dict[str, str]
    """

    _attribute_map = {
        "target_condition": {"key": "targetCondition", "type": "str"},
        "custom_metric_queries": {"key": "customMetricQueries", "type": "{str}"},
    }

    def __init__(self, **kwargs):
        super(ConfigurationQueriesTestInput, self).__init__(**kwargs)
        self.target_condition = kwargs.get("target_condition", None)
        self.custom_metric_queries = kwargs.get("custom_metric_queries", None)
