from unittest.mock import patch

import pytest
from dynamicprompts.generators.randomprompt import RandomPromptGenerator
from dynamicprompts.wildcards import WildcardManager

from tests.samplers.utils import patch_random_sampler_wildcard_choice


@pytest.fixture
def generator(wildcard_manager: WildcardManager) -> RandomPromptGenerator:
    return RandomPromptGenerator(wildcard_manager)


class TestRandomGenerator:
    def test_literal_template(self, generator):
        prompt = "I love bread"

        prompts = list(generator.generate(prompt, 10))

        assert len(prompts) == 10
        assert prompts[0] == prompt

    def test_generate_with_wildcard(self, generator):
        prompt = "I saw a __animals/mammals/*__"  # refers to a real wildcard
        animals = ["dog", "dog", "wolf", "tiger"]  # ... but we'll mock it

        with patch_random_sampler_wildcard_choice(animals):
            prompts = list(generator.generate(prompt, 4))

        assert prompts == [f"I saw a {animal}" for animal in animals]

    def test_without_wildcard_manager(self):
        generator = RandomPromptGenerator()
        assert generator._context.wildcard_manager.path is None

    def test_generate_with_seeds_wrong_length(self, generator: RandomPromptGenerator):
        with pytest.raises(ValueError) as exc_info:
            generator.generate(num_images=2, seeds=[42])
        assert str(exc_info.value) == "Expected 2 seeds, but got 1"

    def test_generate_with_template_and_seeds(self, generator: RandomPromptGenerator):
        with patch.object(generator._context.rand, "seed", autospec=True) as mock_seed:
            generator.generate(template="test_template", num_images=2, seeds=[42, 43])

            mock_seed.assert_any_call(42)
            mock_seed.assert_any_call(43)
