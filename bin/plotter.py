import matplotlib.pyplot as plot


def plot_metrics_list(metrics_list: list):
    threshold_list = []

    precision_list = []
    recall_list = []
    f1_list = []

    for metric in metrics_list:
        threshold_list.append(metric.lsh_threshold)

        precision_list.append(metric.precision)
        recall_list.append(metric.recall)
        f1_list.append(metric.f1)

    plot.plot(threshold_list, precision_list, label="precision")
    plot.plot(threshold_list, recall_list, label="recall")
    plot.plot(threshold_list, f1_list, label="f1")

    plot.ylabel("lsh threshold")
    plot.xlabel("value")

    plot.legend()

    plot.show()
