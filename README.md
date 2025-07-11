# GMTK Maeser
## Overview
GMTK Maeser is a chatbot webapp that uses the Maeser library to pull resources from Mark Brown's game design series, Game Maker's Toolkit.

## Features
- **Conversations Powered by Retrieval-Augmented-Generation (RAG):** When asked a question, the chatbot pulls from a database of GMTK transcripts to find the most relevant resoures, and it uses this data to answer the user's question, referring the user to the videos it sourced its information from.
- **Tools for Creating/Updating the GMTK Database:** The GMTK video transcripts must be converted into a **vectorstore** database to be used by the chatbot. This repository provides various [tools](./tools/) to do so with guided [instructions](./tools/readme.md).

This package is licensed on the LGPL version 3 or later.
See [COPYING.LESSER.md](COPYING.LESSER.md) and [COPYING.md](COPYING.md) for details.

Other resources may be licensed under different compatible licenses, such as the [MIT License](https://opensource.org/license/mit) (Bootstrap Icons), [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/legalcode) (normalize.css), or [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en) (images and vector stores).
