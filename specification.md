# NDES Specification

* **IRI**
    * <https://linked.data.gov.au/def/ndesbd/spec>
* **Title**
    * National Data Exchange Standard's Specifciation
* **Definition**
    * This document lists the normative requirements for data aiming to conform to the [National Data Exchange Standard](https://linked.data.gov.au/def/ndes). It is to be used as the authoratitive, human-readable, identified, list of individual requirements from which other profile artifacts, such as data validators, are derived.
* **Created**
    * 2021-10-24
* **Modified**
    * 2021-10-24
* **Creator**
    * [SURROUND Australia Pty Ltd](https://linked.data.gov.au/org/surround), [Gaia Resources](https://www.gaiaresources.com.au/) and the [Department of Agriculture, Water and the Environment](https://linked.data.gov.au/org/dawe)
* **Publisher**
    * [Department of Agriculture, Water and the Environment](https://linked.data.gov.au/org/dawe)
* **License**
    * [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
* **Further information**
    * This specification is part of the Australian [National Data Exchange Standard](https://linked.data.gov.au/def/ndes). That Standard is established as a _profile_ of multiple other stnadards and is, itself, made of many parts, of which this Specification is only one.
    * See that profile's main document for details of the other profile parts and how this Specification related to them.
                     
## Introduction

This document is a list of _requirements_ for data to meet in order to conform to the [National Data Exchange Standard](https://linked.data.gov.au/def/ndes). Each _requirement_ is defined with a table of values like this:

Property | Value
--- | ---
Identifier | Prefixed IRI identifier
Label | Short text
Definition | Defining text
Conformance Classes | Selected Conformance Class Identifiers
Source | Notes on _requirement_ source
Validators | Related SHACL validators
Examples | Related RDF example data

The [Semantic Web](https://en.wikipedia.org/wiki/Semantic_Web) interpretation of the relation of each of those properties are to each requirement instance are:

Property | Defining RDF predicate | Object type
--- | --- | ---
Identifier | `dcterms:identifier` | IRI
Label | `skos:prefLabel` | text
Definition | `skos:definition` | text
Conformance Classes | `dcterms:isPartOf` | IRIs
Source | `dcterms:source` or `dcterms:provenance` | IRI of an NDES resource or text
Validators | ??? | IRI of a `Resource Descriptor`
Examples | `skos:example` | IRI of a `Resource Descriptor`

See the [Namespaces](#namespaces) section below to understand the prefixes in the table above.

The following subsections define properties of the _requirements_ in detail.

#### Identifier

Each _requirement_ is identified with a unique identifier of the form `req:X`, where `req:` is a prefix for the IRI namespace <https://linked.data.gov.au/def/ndesbd/req/> and `X` is a number, the number of the _requirement_.

The IRI namespace plus the number make the complete IRI of the _requirement_.

An IRI is an [Internationalized Resource Identifier](https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier) which is a globally unique web address created within a managed namespace that resolves to the element it identifies

#### Labeled

Each _requirement_ is named with a short form of its definition, to assist with human referencing.

#### Definition

Each _requirement_ is defined in human-readable terms but with references to data elements modelled according to ontologies defined using the [Web Ontology Language (OWL)](https://www.w3.org/TR/owl2-overview/) since the _target models_ of the NDES are themselves OWL Ontologies.

> NOTE: if there are differences between derivatives of this specification, including the NDES validator, these definitions take precendence

#### Conformance Classes list

Each _requirement_ is categorised within one or more "Conformance Classes" which are defined bundles of requrirements. Within the NDES, the Conformance Classes form modules which data may conform to individually.

Each _requirement_ needs to indicate its Conformance Classes by linking to them.

#### Contains source notes 

Each _requirement_ contains source notes  what motivated the _requirement_'s definition, including references to source documents or other NDES artifacts, such as ontologies.

#### Related validators

Each _requirement_ contains references to individual, identified, data validation _shapes_ defined in the NDES Profile's _validator_ used to validate [Resource Description Framework (RDF)](https://www.w3.org/RDF/) data - the only form of data allowed to be used for NDES data exchange.

The content of _validator_s is contianed in the NDES' _Validator_ resource.

> NOTE: the validating _shapes_ are not 1:1 with these _requirements_ and that there are _requirements_ for which there are no _shapes_ - those _requirements_ that cannot be determined to have been met by inspecting data.

#### Canonical examples

For each _requirement_, references are given to at least two _canonical examples_ of RDF data that do (positive example) and don't (negative example) pass validation using the validators related to the _requirement_.

The content of the _canonical examples_, i.e. the examples' data, is contianed in the NDES' _Canonical Examples_ resource.

## Namespaces

Prefix | Namespace | Description
--- | --- | ---
**`req:`** | **`https://linked.data.gov.au/def/ndesbd/req/`** | **NDES Requirements namespace**
`dcterms:` | `http://purl.org/dc/terms/` | Dublin Core Terms vocabulary namespace
`ex:` | `http://example.com/thing` | Generic examples namespace
`nex:` | `https://linked.data.gov.au/def/ndesbd/examples/` | NDES Canonical Examples namespace
`nsh:` | `https://linked.data.gov.au/def/ndesbd/shape/` | NDES Validators Shapes namespace
`owl:` | `http://www.w3.org/2002/07/owl#` | Web Ontology Language ontology namespace
`rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | RDF Schema ontology namespace
`sosa:` | `http://www.w3.org/ns/sosa/` | Sensor, Observation, Sample, and Actuator ontology namespace
`skos:` | `http://www.w3.org/2004/02/skos/core#` | Simple Knowledge Organization System (SKOS) ontology namespace
`tern:` | `http://www.w3.org/ns/sosa/` | TERN Ontology namespace
`time:` | `http://www.w3.org/2006/time#` | Time Ontology in OWL namespace
`void:` | `http://rdfs.org/ns/void#` | Vocabulary of Interlinked Data (VoID) ontology namespace
`xsd:` | `http://www.w3.org/2001/XMLSchema#` | XML Schema Definitions ontology namespace

## Conformance Classes

Conformance Classes are groupings of Requirements within the NDES. Data claiming conforming to the NDES may indicate conformance per-Conformance Class. Conformance  to a Conformance Class means conforming to _all_ the Requirements within it, not just some.

The Conformance Classes are:

* [cc:tern-ontology](#cctern-ontology)
* [cc:ndes-message](#ccndes-message)

### cc:tern-ontology

Property | Value
--- | ---
Identifier | [`cc:tern-ontology`](https://linked.data.gov.au/def/ndesbd/conformanceclass/tern-ontology)
Label | TERN Ontology Conformance Class
Definition | The set of requirements needed to be met to ensure conformance with the TERN Ontology
Requirements | [`req:observation-properties`](https://linked.data.gov.au/def/ndesbd/req/observation-properties)

### cc:ndes-messages

Property | Value
--- | ---
Identifier | [`cc:ndes-messages`](https://linked.data.gov.au/def/ndesbd/conformanceclass/ndes-messages)
Label | NDES Messages Conformance Class
Definition | The set of requirements needed to be met to ensure conformance with the NDES' Gateway's message needs
Requirements | [`req:message-new-observations`](https://linked.data.gov.au/def/ndesbd/req/message-new-observations)


## Requirements

Requirements are the individual rules that data claiming conformance to the NDES must abide by. 

The Requirements are:

* [req:observation-properties](reqobservation-properties)

### TERN Ontology Conformance Class Requirements

#### req:observation-properties

Property | Value
--- | ---
Identifier | [`req:observation-properties`](https://linked.data.gov.au/def/ndesbd/req/observation-properties)
Label | TERN Observation Properties
Definition | Instances of the TERN Ontology's `Observation` class _MUST_ have:<br />* exactly 1 TERN Ontology `inDataset` predicate indicating a TERN Ontology `RDFDataset` class instance;<br />* exactly 1 SOSA Ontology `hasFeatureOfInterest` predicate indicating a TERN Ontology `FeatureOfInterest` class instance;<br />* exactly 1 SOSA Ontology `hasResult` predicate TERN Ontology `Value` class instance;<br />* exactly 1 SOSA Ontology `observedProperty` predicate indicating an IRI;<br />* exactly 1 SOSA Ontology `phenomenonTime` predicate indicating a TIME Ontology `Instant` class instance;<br />* exactly 1 SOSA Ontology `resultTime` predicate indicating a `dateTime` literal value;<br />* exactly 1 SOSA Ontology `usedProcedure` predicate indicating an IRI;<br />* a maximum of 1 Dublin Core Terms `type` predicate indicating an IRI;<br />* a maximum of 1 RDFS Ontology `comment` predicate indicating a `string` literal value;<br />* a maximum of 1 TERN Ontology `hasSiteVisit` predicate indicating a TERN Ontology `SiteVisit` class instance.<br /><br />If the instance has:<br />* a Dublin Core Terms `identifier` predicate it must indicate a `string` literal value;<br />* a GeoSPARQL Ontology `hasGeometry` predicate it must indicate a TERN Location Ontology `Geometry` class instance;<br />* a PROV Ontology `wasAttributedTo` predicate it must indicate a TERN Organisation Ontology `Person` class instance;<br />* a TERN Ontology `hasAttribute` predicate it must indicate an IRI;<br />* a TERN Ontology `usedInstrument` predicate it must indicate a TERN Organisation Ontology `Instrument` class instance.
Conformance Classes | [`cc:1`](https://linked.data.gov.au/def/ndesbd/cc/1)
Source | [TERN Ontology](https://w3id.org/tern/ontologies/tern)
Validators | [`tern:Observation`](https://w3id.org/tern/ontologies/tern/Observation)
Examples | [`ex:observation-valid-01`](https://linked.data.gov.au/def/ndesbd/examples/observation-valid-01)

#### req:2

Property | Value
--- | ---
Identifier | [`req:2`](https://linked.data.gov.au/def/ndesbd/req/2)
Label | Text
Definition | Text
Conformance Classes | [`cc:1`](https://linked.data.gov.au/def/ndesbd/cc/1)
Source | Text
Validators | [`nsh:1`](https://linked.data.gov.au/def/ndesbd/shape/2)
Examples | [`nex:1`](https://linked.data.gov.au/def/ndesbd/examples/3)<br />[`nex:2`](https://linked.data.gov.au/def/ndesbd/examples/4)

#### req:3

Property | Value
--- | ---
Identifier | [`req:3`](https://linked.data.gov.au/def/ndesbd/req/3)
Label | Text
Definition | Text
Conformance Classes | [`cc:2`](https://linked.data.gov.au/def/ndesbd/cc/2)
Source | Text
Validators | [`nsh:1`](https://linked.data.gov.au/def/ndesbd/shape/3)
Examples | [`nex:1`](https://linked.data.gov.au/def/ndesbd/examples/5)<br />[`nex:2`](https://linked.data.gov.au/def/ndesbd/examples/6)

### NDES Message Conformance Class Requirements

#### req:message-new-observations

Property | Value
--- | ---
Identifier | [`req:message-new-observations`](https://linked.data.gov.au/def/ndesbd/req/message-new-observations)
Label | Message containing new Observations
Definition | Instances of the NDES Ontology's `NewObservationsMessage` class _MUST_ contain:<br />* a minimum of 1 RDFS Ontology `member` predicate indicating a SOSA Ontology `ObservationCollection` class instance;<br />* exactly 1 NDES Ontology `targetDataset` predicate indicating a TERN Ontology `RDFDataset` class instance.
Conformance Classes | [`cc:ndes-messages`](https://linked.data.gov.au/def/ndesbd/conformanceclass/ndes-messages)
Source | NDES-BD Gateway Messaging
Validators | [`nsh:message-new-observations-01`](https://linked.data.gov.au/def/ndesbd/shape/message-new-observations-01)
Examples | [`https://linked.data.gov.au/dataset/bdr/message/example-new-valid-01`](https://linked.data.gov.au/dataset/bdr/message/example-new-valid-01)

#### req:message-delete-observations

Property | Value
--- | ---
Identifier | [`req:message-delete-observations`](https://linked.data.gov.au/def/ndesbd/req/message-delete-observations)
Label | Message containing Observation to be deleted
Definition | Instances of the NDES Ontology's `DeleteObservationsMessage` class _MUST_ contain:<br />* a minimum of 1 RDFS Ontology `member` predicate indicating a SOSA Ontology `ObservationCollection` class instance;<br />* the SOSA Ontology `ObservationCollection` class instance must contain a minimum of 1 RDFS Ontology `member` predicate indcating an IRI of an existing TERN Ontology `Observation` class instance`.
Conformance Classes | [`cc:ndes-messages`](https://linked.data.gov.au/def/ndesbd/conformanceclass/ndes-messages)
Source | NDES-BD Gateway Messaging
Validators | [`nsh:message-delete-observations-01`](https://linked.data.gov.au/def/ndesbd/shape/message-delete-observations-01)
Examples | [`https://linked.data.gov.au/dataset/bdr/message/example-delete-valid-01`](https://linked.data.gov.au/dataset/bdr/message/example-delete-valid-01)
