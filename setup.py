from setuptools import setup
exec(open("spynnaker/pyNN/_version.py").read())

setup(
    name="sPyNNaker",
    version=__version__,
    description="Spinnaker implementation of PyNN",
    url="https://github.com/SpiNNakerManchester/SpyNNaker",
    packages=['spynnaker',
              'spynnaker.pyNN',
              'spynnaker.pyNN.model_binaries',
              'spynnaker.pyNN.models',
              'spynnaker.pyNN.models.abstract_models',
              'spynnaker.pyNN.models.abstract_models.abstract_model_components',
              'spynnaker.pyNN.models.abstract_models.buffer_models',
              'spynnaker.pyNN.models.common_objects',
              'spynnaker.pyNN.models.components',
              'spynnaker.pyNN.models.components.input_components',
              'spynnaker.pyNN.models.components.model_components',
              'spynnaker.pyNN.models.components.neuron_components',
              'spynnaker.pyNN.models.components.synapse_shape_components',
              'spynnaker.pyNN.models.delay_extension',
              'spynnaker.pyNN.models.neural_models',
              'spynnaker.pyNN.models.neural_projections',
              'spynnaker.pyNN.models.neural_projections.connectors',
              'spynnaker.pyNN.models.neural_properties',
              'spynnaker.pyNN.models.neural_properties.master_pop_table_generators',
              'spynnaker.pyNN.models.neural_properties.synapse_dynamics',
              'spynnaker.pyNN.models.neural_properties.synapse_dynamics.abstract_rules',
              'spynnaker.pyNN.models.neural_properties.synapse_dynamics.dependences',
              'spynnaker.pyNN.models.spike_source',
              'spynnaker.pyNN.models.utility_models',
              'spynnaker.pyNN.overridden_pacman_functions',
              'spynnaker.pyNN.utilities',
              'spynnaker.pyNN.utilities.conf',
              'spynnaker.pyNN.utilities.database'],
    package_data={'spynnaker.pyNN.model_binaries': ['*.aplx'],
                  'spynnaker': ['spynnaker.cfg'],
                  'spynnaker.pyNN.utilities.conf': ['spynnaker.cfg.template']},
    install_requires=['SpiNNMachine >= 2015.003',
                      'SpiNNMan >= 2015.003',
                      'SpiNNaker_PACMAN >= 2015.003',
                      'SpiNNaker_DataSpecification >= 2015.003',
                      'SpiNNFrontEndCommon >= 2015.001',
                      'pyNN >= 0.7, < 0.8', 'numpy', 'scipy', 'lxml', 'six']
)
