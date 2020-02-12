from abc import ABC, abstractmethod
from typing import (AnyStr, List, Optional)

from core.evaluation import EvaluationStrategy
from core.model import LogRegression


class Node(ABC):
    def __init__(self, nodes_from: Optional[List['Node']],
                 nodes_to: Optional[List['Node']], data_stream,
                 eval_strategy: EvaluationStrategy):
        self.nodes_from = nodes_from
        self.nodes_to = nodes_to
        self.last_parents_ids: Optional[List[AnyStr]]
        self.cached_result = data_stream
        self.eval_strategy = eval_strategy

    @abstractmethod
    def apply(self):
        return self.eval_strategy.evaluate(self.cached_result)


class NodeFactory:
    def log_reg(self):
        eval_strategy = EvaluationStrategy(model=LogRegression())
        return PrimaryNode(nodes_from=None, nodes_to=None, data_stream=None,
                           eval_strategy=eval_strategy)

    def default_xgb(self):
        raise NotImplementedError()

    def lin_reg(self):
        raise NotImplementedError()

    def nemo(self):
        raise NotImplementedError()


class PrimaryNode(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply(self):
        return self.eval_strategy.evaluate(self.cached_result)


class SecondaryNode(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply(self):
        return self.eval_strategy.evaluate(self.cached_result)
