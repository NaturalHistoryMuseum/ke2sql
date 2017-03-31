#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '14/03/2017'.



"""

import luigi
from operator import is_not
from ke2sql.tasks.dataset import DatasetTask
from ke2sql.lib.operators import is_one_of, is_not_one_of
from ke2sql.lib.field import Field, MetadataField
from ke2sql.lib.filter import Filter
from ke2sql.lib.config import Config


class SpecimenDatasetTask(DatasetTask):

    package_name = 'collection-specimens'
    package_description = "Specimen records from the Natural History Museum\'s collection"
    package_title = "Collection specimens"

    resource_title = 'Specimen records'
    resource_id = Config.get('resource_ids', 'specimen')
    resource_description = 'Specimen records'
    resource_type = 'dwc'  # Darwin Core

    fields = DatasetTask.fields + [
        # Update fields
        Field('ecatalogue', 'AdmDateModified', 'dateModified'),
        Field('ecatalogue', 'AdmDateInserted', 'dateCreated'),
        Field('ecatalogue', 'AdmGUIDPreferredValue', 'occurrenceID'),
        # Record numbers
        Field('ecatalogue', 'DarCatalogNumber', 'catalogNumber'),
        # Used if DarCatalogueNumber is empty
        Field('ecatalogue', 'RegRegistrationNumber', 'catalogNumber'),
        # Taxonomy
        Field('ecatalogue', 'DarScientificName', 'scientificName'),
        # Rather than using the two darwin core fields DarScientificNameAuthorYear and ScientificNameAuthor
        # It's easier to just use IdeFiledAsAuthors which has them both concatenated
        Field('ecatalogue', 'IdeFiledAsAuthors', 'scientificNameAuthorship'),
        Field('ecatalogue', 'DarTypeStatus', 'typeStatus'),
        # If DarTypeStatus is empty, we'll use sumTypeStatus which has previous determinations
        Field('ecatalogue', 'sumTypeStatus', 'typeStatus'),
        # Use nearest name place rather than precise locality https://github', 'com/NaturalHistoryMuseum/ke2mongo/issues/29
        Field('ecatalogue', 'PalNearestNamedPlaceLocal', 'locality'),
        # Locality if nearest named place is empty
        # The encoding of DarLocality is buggered - see 1804973
        # So better to use the original field with the correct encoding
        Field('ecatalogue', 'sumPreciseLocation', 'locality'),
        # Locality if precise and nearest named place is empty
        Field('ecatalogue', 'MinNhmVerbatimLocalityLocal', 'locality'),
        Field('ecatalogue', 'DarCountry', 'country'),
        Field('ecatalogue', 'DarWaterBody', 'waterBody'),
        Field('ecatalogue', 'EntLocExpeditionNameLocal', 'expedition'),
        Field('ecatalogue', 'sumParticipantFullName', 'recordedBy'),
        Field('ecatalogue', 'ColDepartment', 'collectionCode'),
        # Taxonomy
        Field('ecatalogue', 'DarScientificName', 'scientificName'),
        Field('ecatalogue', 'DarKingdom', 'kingdom'),
        Field('ecatalogue', 'DarPhylum', 'phylum'),
        Field('ecatalogue', 'DarClass', 'class'),
        Field('ecatalogue', 'DarOrder', 'order'),
        Field('ecatalogue', 'DarFamily', 'family'),
        Field('ecatalogue', 'DarGenus', 'genus'),
        Field('ecatalogue', 'DarSubgenus', 'subgenus'),
        Field('ecatalogue', 'DarSpecies', 'specificEpithet'),
        Field('ecatalogue', 'DarSubspecies', 'infraspecificEpithet'),
        Field('ecatalogue', 'DarHigherTaxon', 'higherClassification'),
        Field('ecatalogue', 'DarInfraspecificRank', 'taxonRank'),
        # Location
        Field('ecatalogue', 'DarStateProvince', 'stateProvince'),
        Field('ecatalogue', 'DarContinent', 'continent'),
        Field('ecatalogue', 'DarIsland', 'island'),
        Field('ecatalogue', 'DarIslandGroup', 'islandGroup'),
        Field('ecatalogue', 'DarHigherGeography', 'higherGeography'),
        Field('ecatalogue', 'ColHabitatVerbatim', 'habitat'),
        Field('ecatalogue', 'DarDecimalLongitude', 'decimalLongitude'),
        Field('ecatalogue', 'DarDecimalLatitude', 'decimalLatitude'),
        Field('ecatalogue', 'sumPreferredCentroidLongitude', 'verbatimLongitude'),
        Field('ecatalogue', 'sumPreferredCentroidLatitude', 'verbatimLatitude'),
        Field('ecatalogue', 'DarGeodeticDatum', 'geodeticDatum'),
        Field('ecatalogue', 'DarGeorefMethod', 'georeferenceProtocol'),
        # Occurrence
        Field('ecatalogue', 'DarMinimumElevationInMeters', 'minimumElevationInMeters'),
        Field('ecatalogue', 'DarMaximumElevationInMeters', 'maximumElevationInMeters'),
        Field('ecatalogue', 'DarMinimumDepthInMeters', 'minimumDepthInMeters'),
        Field('ecatalogue', 'DarMaximumDepthInMeters', 'maximumDepthInMeters'),
        Field('ecatalogue', 'CollEventFromMetres', 'minimumDepthInMeters'),
        Field('ecatalogue', 'CollEventToMetres', 'maximumDepthInMeters'),
        Field('ecatalogue', 'DarCollectorNumber', 'recordNumber'),
        Field('ecatalogue', 'DarIndividualCount', 'individualCount'),
        # Duplicate lifeStage fields - only fields with a value get populated so
        # there is no risk in doing this
        Field('ecatalogue', 'DarLifeStage', 'lifeStage'),
        # Parasite cards use a different field for life stage
        Field('ecatalogue', 'CardParasiteStage', 'lifeStage'),
        Field('ecatalogue', 'DarSex', 'sex'),
        Field('ecatalogue', 'DarPreparations', 'preparations'),
        # Identification
        Field('ecatalogue', 'DarIdentifiedBy', 'identifiedBy'),
        # KE Emu has 3 fields for identification date: DarDayIdentified, DarMonthIdentified and DarYearIdentified
        # But EntIdeDateIdentified holds them all - which is what we want for dateIdentified
        Field('ecatalogue', 'EntIdeDateIdentified', 'dateIdentified'),
        Field('ecatalogue', 'DarIdentificationQualifier', 'identificationQualifier'),
        Field('ecatalogue', 'DarTimeOfDay', 'eventTime'),
        Field('ecatalogue', 'DarDayCollected', 'day'),
        Field('ecatalogue', 'DarMonthCollected', 'month'),
        Field('ecatalogue', 'DarYearCollected', 'year'),
        # Geology
        Field('ecatalogue', 'DarEarliestEon', 'earliestEonOrLowestEonothem'),
        Field('ecatalogue', 'DarLatestEon', 'latestEonOrHighestEonothem'),
        Field('ecatalogue', 'DarEarliestEra', 'earliestEraOrLowestErathem'),
        Field('ecatalogue', 'DarLatestEra', 'latestEraOrHighestErathem'),
        Field('ecatalogue', 'DarEarliestPeriod', 'earliestPeriodOrLowestSystem'),
        Field('ecatalogue', 'DarLatestPeriod', 'latestPeriodOrHighestSystem'),
        Field('ecatalogue', 'DarEarliestEpoch', 'earliestEpochOrLowestSeries'),
        Field('ecatalogue', 'DarLatestEpoch', 'latestEpochOrHighestSeries'),
        Field('ecatalogue', 'DarEarliestAge', 'earliestAgeOrLowestStage'),
        Field('ecatalogue', 'DarLatestAge', 'latestAgeOrHighestStage'),
        Field('ecatalogue', 'DarLowestBiostrat', 'lowestBiostratigraphicZone'),
        Field('ecatalogue', 'DarHighestBiostrat', 'highestBiostratigraphicZone'),
        Field('ecatalogue', 'DarGroup', 'group'),
        Field('ecatalogue', 'DarFormation', 'formation'),
        Field('ecatalogue', 'DarMember', 'member'),
        Field('ecatalogue', 'DarBed', 'bed'),
        # These fields do not map to DwC, but are still very useful
        Field('ecatalogue', 'ColSubDepartment', 'subDepartment'),
        Field('ecatalogue', 'PrtType', 'partType'),
        Field('ecatalogue', 'RegCode', 'registrationCode'),
        Field('ecatalogue', 'CatKindOfObject', 'kindOfObject'),
        Field('ecatalogue', 'CatKindOfCollection', 'kindOfCollection'),
        Field('ecatalogue', 'CatPreservative', 'preservative'),
        # Used if CatPreservative is empty
        Field('ecatalogue', 'EntCatPreservation', 'preservative'),
        Field('ecatalogue', 'ColKind', 'collectionKind'),
        Field('ecatalogue', 'EntPriCollectionName', 'collectionName'),
        Field('ecatalogue', 'PalAcqAccLotDonorFullName', 'donorName'),
        Field('ecatalogue', 'DarPreparationType', 'preparationType'),
        Field('ecatalogue', 'DarObservedWeight', 'observedWeight'),
        # Location
        # Data is stored in sumViceCountry field in ecatalogue data - but actually this
        # should be viceCountry Field(which it is in esites)
        Field('ecatalogue', 'sumViceCountry', 'viceCounty'),
        # DNA
        Field('ecatalogue', 'DnaExtractionMethod', 'extractionMethod'),
        Field('ecatalogue', 'DnaReSuspendedIn', 'resuspendedIn'),
        Field('ecatalogue', 'DnaTotalVolume', 'totalVolume'),
        # Parasite card
        Field('ecatalogue', 'EntCatBarcode', 'barcode'),
        Field('ecatalogue', 'CardBarcode', 'barcode'),
        # Egg
        Field('ecatalogue', 'EggClutchSize', 'clutchSize'),
        Field('ecatalogue', 'EggSetMark', 'setMark'),
        # Nest
        Field('ecatalogue', 'NesShape', 'nestShape'),
        Field('ecatalogue', 'NesSite', 'nestSite'),
        # Silica gel
        Field('ecatalogue', 'SilPopulationCode', 'populationCode'),
        # Botany
        Field('ecatalogue', 'CollExsiccati', 'exsiccati'),
        Field('ecatalogue', 'ColExsiccatiNumber', 'exsiccatiNumber'),
        Field('ecatalogue', 'ColSiteDescription', 'labelLocality'),
        Field('ecatalogue', 'ColPlantDescription', 'plantDescription'),
        Field('ecatalogue', 'FeaCultivated', 'cultivated'),
        # Paleo
        Field('ecatalogue', 'PalDesDescription', 'catalogueDescription'),
        Field('ecatalogue', 'PalStrChronostratLocal', 'chronostratigraphy'),
        Field('ecatalogue', 'PalStrLithostratLocal', 'lithostratigraphy'),
        # Mineralogy
        Field('ecatalogue', 'MinDateRegistered', 'dateRegistered'),
        Field('ecatalogue', 'MinIdentificationAsRegistered', 'identificationAsRegistered'),
        Field('ecatalogue', 'MinIdentificationDescription', 'identificationDescription'),
        Field('ecatalogue', 'MinPetOccurance', 'occurrence'),
        Field('ecatalogue', 'MinOreCommodity', 'commodity'),
        Field('ecatalogue', 'MinOreDepositType', 'depositType'),
        Field('ecatalogue', 'MinTextureStructure', 'texture'),
        Field('ecatalogue', 'MinIdentificationVariety', 'identificationVariety'),
        Field('ecatalogue', 'MinIdentificationOther', 'identificationOther'),
        Field('ecatalogue', 'MinHostRock', 'hostRock'),
        Field('ecatalogue', 'MinAgeDataAge', 'age'),
        Field('ecatalogue', 'MinAgeDataType', 'ageType'),
        # Mineralogy location
        Field('ecatalogue', 'MinNhmTectonicProvinceLocal', 'tectonicProvince'),
        Field('ecatalogue', 'MinNhmStandardMineLocal', 'mine'),
        Field('ecatalogue', 'MinNhmMiningDistrictLocal', 'miningDistrict'),
        Field('ecatalogue', 'MinNhmComplexLocal', 'mineralComplex'),
        Field('ecatalogue', 'MinNhmRegionLocal', 'geologyRegion'),
        # Meteorite
        Field('ecatalogue', 'MinMetType', 'meteoriteType'),
        Field('ecatalogue', 'MinMetGroup', 'meteoriteGroup'),
        Field('ecatalogue', 'MinMetChondriteAchondrite', 'chondriteAchondrite'),
        Field('ecatalogue', 'MinMetClass', 'meteoriteClass'),
        Field('ecatalogue', 'MinMetPetType', 'petrologyType'),
        Field('ecatalogue', 'MinMetPetSubtype', 'petrologySubtype'),
        Field('ecatalogue', 'MinMetRecoveryFindFall', 'recovery'),
        Field('ecatalogue', 'MinMetRecoveryDate', 'recoveryDate'),
        Field('ecatalogue', 'MinMetRecoveryWeight', 'recoveryWeight'),
        Field('ecatalogue', 'MinMetWeightAsRegistered', 'registeredWeight'),
        Field('ecatalogue', 'MinMetWeightAsRegisteredUnit', 'registeredWeightUnit'),
        # Determinations
        Field('ecatalogue', 'IdeCitationTypeStatus', 'determinationTypes'),
        Field('ecatalogue', 'EntIdeScientificNameLocal', 'determinationNames'),
        Field('ecatalogue', 'EntIdeFiledAs', 'determinationFiledAs'),
        # Project
        Field('ecatalogue', 'NhmSecProjectName', 'project'),
    ]

    # Combine filters with default dataset task filters
    filters = DatasetTask.filters + [
        # Records must have a GUID
        Filter('ecatalogue', 'AdmGUIDPreferredValue', [
            (is_not, None)
        ]),
        # Does this record have an excluded status - Stub etc.,
        Filter('ecatalogue', 'SecRecordStatus', [
            (is_not, None),
            (is_not_one_of, [
                "DELETE",
                "DELETE-MERGED",
                "DUPLICATION",
                "Disposed of",
                "FROZEN ARK",
                "INVALID",
                "POSSIBLE TYPE",
                "PROBLEM",
                "Re-registered in error",
                "Reserved",
                "Retired",
                "Retired (see Notes)",
                "Retired (see Notes)Retired (see Notes)",
                "SCAN_cat",
                "See Notes",
                "Specimen missing - see notes",
                "Stub",
                "Stub Record",
                "Stub record"
            ])
        ]),
        # Record must be in one of the known collection departments
        # (Otherwise the home page breaks)
        Filter('ecatalogue', 'ColDepartment', [
            (is_one_of, [
                "Botany",
                "Entomology",
                "Mineralogy",
                "Palaeontology",
                "Zoology"
            ])
        ]),
        Filter('ecatalogue', 'ColRecordType', [
            (is_one_of, [
                'Specimen',
                'Specimen - single',
                "Specimen - multiple",
                'DNA Prep',
                'Mammal Group Parent',
                'Mammal Group Part',
                "Bird Group Parent",
                "Bird Group Part",
                'Bryozoa Part Specimen',
                'Silica Gel Specimen',
                "Parasite Card",
            ]),
        ])
    ]

    # Extra metadata fields, used to build the dataset views (JOINS etc.,)
    metadata_fields = DatasetTask.metadata_fields + [
        # Extra column field mappings - not included in properties, have a column in their own right
        MetadataField('ecatalogue', 'MulMultiMediaRef', 'multimedia_irns', "INTEGER[]"),
        MetadataField('ecatalogue', 'ColRecordType', 'record_type', "TEXT"),
        MetadataField('ecatalogue', 'RegRegistrationParentRef', 'parent_irn', "INTEGER"),
        MetadataField('ecatalogue', 'CardParasiteRef', 'parasite_taxonomy_irn', "INTEGER"),
    ]

    def dataset_record_types(self):
        """
        Override the dataset record types, as we don;t actually include the
        And of the parent types:
            Bird Group Parent
            Mammal Group Parent
        :return:
        """
        parent_types = [
            'Bird Group Parent',
            'Mammal Group Parent',
        ]
        record_types = super(SpecimenDatasetTask, self).dataset_record_types()
        # Return a list with parent types removed
        return [record_type for record_type in record_types if record_type not in parent_types]

    def pre_query(self, connection):
        """
        Queries to tidy up the data before building the dataset view
        """
        cursor = connection.cursor()

        max_lat_lon = [
            ('decimalLatitude', 90),
            ('decimalLongitude', 180)
        ]
        # Generate SQL statements for removing all properties
        for property_name, max_value in max_lat_lon:
            sql = """
                UPDATE ecatalogue SET properties = properties - '{property_name}'
                WHERE cast(ecatalogue.properties->>'{property_name}' as FLOAT8) < -{max_value}
                OR cast(ecatalogue.properties->>'{property_name}' as FLOAT8) > {max_value}
            """.format(
                property_name=property_name,
                max_value=max_value
            )
            cursor.execute(sql)

    def get_query(self):
        """
        Override get_query to add join to etaxonomy table
        :return:
        """
        query = super(SpecimenDatasetTask, self).get_query()
        # Add geom field
        query[query.index('SELECT') + 1].append(
            """st_setsrid(
                st_makepoint(
                    cast(ecatalogue.properties->>'decimalLongitude' as FLOAT8),
                    cast(ecatalogue.properties->>'decimalLatitude' as FLOAT8)
                ), 4326) as _geom
            """
        )
        # Add webmercator projection geom field
        query[query.index('SELECT') + 1].append(
            """st_transform(
                    st_setsrid(
                        st_makepoint(
                        cast(ecatalogue.properties->>'decimalLongitude' as FLOAT8),
                        cast(ecatalogue.properties->>'decimalLatitude' as FLOAT8)
                        ),
                    4326),
                3857) as _the_geom_webmercator
            """
        )
        return query

if __name__ == "__main__":
    luigi.run(main_task_cls=SpecimenDatasetTask)
