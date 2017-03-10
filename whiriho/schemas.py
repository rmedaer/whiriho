# -*- coding: utf-8 -*-

__whiriho_catalog__ = {
    'type': 'object',
    'properties': {
        'version': {
            'type': 'string'
        }
    },
    'required': [
        'version'
    ],
    'additionalProperties': True
}
__whiriho_catalog_v1__ = {
    'type': 'object',
    'properties': {
        'version': {
            'type': 'string',
        },
        'catalog': {
            'type': 'object',
            'additionalProperties': {
                'type': 'object',
                'properties': {
                    'uri': {
                        'type': 'string'
                    },
                    'format': {
                        'enum': ['yaml', 'json', 'ini']
                    },
                    'schema': {
                        'type': 'string'
                    },
                    'title': {
                        'type': 'string'
                    },
                    'description': {
                        'type': 'string'
                    }
                },
                'required': [
                    'uri'
                ]
            }
        }
    },
    'required': [
        'version',
        'catalog'
    ],
    'additionalProperties': False
}
