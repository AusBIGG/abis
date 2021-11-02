# NDES Specification

* **IRI**
    * <https://linked.data.gov.au/def/ndes/spec>
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

Each _requirement_ is identified with a unique identifier of the form `req:X`, where `req:` is a prefix for the IRI namespace <https://linked.data.gov.au/def/ndes/req/> and `X` is a number, the number of the _requirement_.

The IRI namespace plus the number make the complete IRI of the _requirement_.

An IRI is an [Internationalized Resource Identifier](https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier) which is a globally unique web address created within a managed namespace that resolves to the element it identifies

#### Labeled

Each _requirement_ is named with a short form of its definition, to assist with human referencing.

#### Definition

Each _requirement_ is defined in human-readable terms but with references to data elements modelled according to ontologies defined using the [Web Ontology Language (OWL)](https://www.w3.org/TR/owl2-overview/) since the _target models_ of the NDES are themselves OWL Ontologies.

> NOTE: if there are differences between derivatives of this specification, including the NDES validator, these definitions take precendence

#### Conformance Classes list

Each _requirement_ is categorised within one or more "Conformance Classes" which are defined bundles of requrirements. Within the NDES, the Conformance Classes form modules which data may conform to individually.

Each _requirement_ needs to indicate its Conformance Classes by just linking to them.

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
**`req:`** | **`https://linked.data.gov.au/def/ndes/req/`** | **NDES Requirements namespace**
`dcterms:` | `http://purl.org/dc/terms/` | Dublin Core Terms vocabulary namespace
`eg:` | `https://linked.data.gov.au/def/ndes/eg/` | NDES Canonical Examples namespace
`shp:` | `https://linked.data.gov.au/def/ndes/shape/` | NDES alidator Shapes namespace
`skos:` | `http://www.w3.org/2004/02/skos/core#` | Simple Knowledge Organization System (SKOS) ontology namespace

## Requirements

### req:1

Property | Value
--- | ---
Identifier | [`req:1`](https://linked.data.gov.au/def/ndes/req/1)
Label | Text
Definition | Text
Conformance Classes | [`cc:1`](https://linked.data.gov.au/def/ndes/cc/1)
Source | Text
Validators | [`shp:1`](https://linked.data.gov.au/def/ndes/shape/1)
Examples | [`eg:1`](https://linked.data.gov.au/def/ndes/eg/1)<br />[`eg:2`](https://linked.data.gov.au/def/ndes/eg/2)

### req:2

Property | Value
--- | ---
Identifier | [`req:2`](https://linked.data.gov.au/def/ndes/req/2)
Label | Text
Definition | Text
Conformance Classes | [`cc:1`](https://linked.data.gov.au/def/ndes/cc/1)
Source | Text
Validators | [`shp:1`](https://linked.data.gov.au/def/ndes/shape/2)
Examples | [`eg:1`](https://linked.data.gov.au/def/ndes/eg/3)<br />[`eg:2`](https://linked.data.gov.au/def/ndes/eg/4)

### req:3

Property | Value
--- | ---
Identifier | [`req:3`](https://linked.data.gov.au/def/ndes/req/3)
Label | Text
Definition | Text
Conformance Classes | [`cc:2`](https://linked.data.gov.au/def/ndes/cc/2)
Source | Text
Validators | [`shp:1`](https://linked.data.gov.au/def/ndes/shape/3)
Examples | [`eg:1`](https://linked.data.gov.au/def/ndes/eg/5)<br />[`eg:2`](https://linked.data.gov.au/def/ndes/eg/6)

### req:4

Property | Value
--- | ---
Identifier | [`req:4`](https://linked.data.gov.au/def/ndes/req/4)
Label | Text
Definition | Text
Conformance Classes | [`cc:3`](https://linked.data.gov.au/def/ndes/cc/3)
Source | Text
Validators | [`shp:1`](https://linked.data.gov.au/def/ndes/shape/3)
Examples | [`eg:1`](https://linked.data.gov.au/def/ndes/eg/7)<br />[`eg:2`](https://linked.data.gov.au/def/ndes/eg/8)
