import matplotlib.pyplot as plot


def plot_metrics(metrics_dict: dict, xlabel):
    """
    Plots graphs based on dict of Metrics objects.
    Plots multiple graphs on the same plot, where axis x is lsh algorithm threshold.

    :param metrics_list: list of Metrics objects from bin.metric_analysis.metrics
    :return:
    """
    xvalues = metrics_dict.keys()
    metrics_list = metrics_dict.values()

    precision_list = []
    recall_list = []
    f1_list = []

    for metric in metrics_list:
        precision_list.append(metric.precision)
        recall_list.append(metric.recall)
        f1_list.append(metric.f1)

    plot.plot(xvalues, precision_list, label="precision")
    plot.plot(xvalues, recall_list, label="recall")
    plot.plot(xvalues, f1_list, label="f1")

    plot.xlabel(xlabel)
    plot.ylabel("value")

    plot.legend()

    plot.show()
