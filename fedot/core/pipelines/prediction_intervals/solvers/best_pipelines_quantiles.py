from typing import Union

from golem.core.log import LoggerAdapter
from fedot.core.data.data import InputData
from fedot.api.main import Fedot
from fedot.core.pipelines.adapters import PipelineAdapter

from fedot.core.pipelines.prediction_intervals.utils import get_different_pipelines


def solver_best_pipelines_quantiles(train_input: InputData,
                           model: Fedot,
                           logger: LoggerAdapter,
                           horizon: int,
                           number_models: Union[int, str],
                           show_progress: bool):
    """This function realizes 'best_pipelines_quantiles' method.

    Args:
        train_input (InputData): train time series
        model (Fedot): given Fedot class object
        logger: prediction interval logger
        horizon (int): horizon to build forecast
        number_models (Union[int,str]): number pipelines from last generation to use
        show_progress (bool): flag to show progress
        logger: prediction intervals logger

    Returns:
        a list of predictions to build prediction intervals.
    """

    # take best pipelines from the last generation
    all_pipelines = get_different_pipelines(model.history.individuals[-2])
    number_avaliable_pipelines = len(all_pipelines)
    predictions = []
    s = 1
    message = f'All {number_avaliable_pipelines} avaliable pipelines will be used for training.'

    if number_models == 'max':
        index_iterations = number_avaliable_pipelines
        if show_progress:
            logger.info(message)
    elif number_models > number_avaliable_pipelines:
        index_iterations = number_avaliable_pipelines
        if show_progress:
            logger.info('number_models > number of avaliable pipelines. ' + message)
    else:
        index_iterations = number_models
        if show_progress:
            logger.info(f'{number_models} best pipelines will be used for training.')

    for ind in all_pipelines[:index_iterations]:

        pipeline = PipelineAdapter().restore(ind.graph)
        if show_progress:
            logger.info(f'Fitting pipeline №{s}')
            s += 1
            pipeline.show()
        model.current_pipeline = pipeline
        pipeline.fit(train_input)
        preds = model.forecast(horizon=horizon)
        predictions.append(preds)

    return predictions
