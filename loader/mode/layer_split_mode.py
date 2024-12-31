from oba import Obj

from loader.pager.llm_split_pager import LLMSplitPager
from loader.mode.base_mode import BaseMode
from model.operators.base_llm_operator import BaseLLMOperator


class LayerSplitMode(BaseMode):
    load_model = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.resampler = self.manager.resampler
        self.layers = Obj.raw(self.manager.exp.store.layers)
        self.page_size = self.manager.exp.policy.batch_size
        self.store_dir = self.manager.exp.store.dir

    def work(self, *args, **kwargs):
        item_encoder = self.legommender.item_op
        assert isinstance(item_encoder, BaseLLMOperator), ValueError(f'item_encoder is not a LLMOperator')

        pager = LLMSplitPager(
            inputer=item_encoder.inputer,
            layers=self.layers,
            hidden_size=item_encoder.config.input_dim,
            contents=self.resampler.item_cache,
            model=item_encoder.get_all_hidden_states,
            page_size=self.page_size,
        )

        pager.run()
        pager.store(self.store_dir)
