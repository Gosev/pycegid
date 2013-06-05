# -*- coding: utf-8 -*-
##############################################################################
#
#    PyCEGID is a library to export datas in TRA format
#    Copyright (C) 2013 SYLEAM (<http://syleam.fr>) Christophe CHAUVET
#
#    This file is a part of PyCEGID
#
#    PyCEGID is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PyCEGID is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time


class VersionNotFound(Exception):
    pass


class HeaderNotFound(Exception):
    pass


class MandatoryException(Exception):
    pass


class ExportTra(object):
    """
    Generate format for Cegid
    """

    _default_version = '007'
    _default_date = '01011900'
    _current_date = time.strftime('%Y%m%d%H%M')
    _zone_fixe = '***'

    _available_version = ['007']
    _generate_date = ''

    _debug_header = 0

    _content = {
        'header': '',
        'lines': [],
    }

    def __init__(self):
        """
        Instanciate the class, and initialise the amount to Zero
        """
        self._total = 0.0
        self._generate_date = time.strftime('%d%m%Y%H%M')

    # TODO: add function to change date for the generate file

    def changeFormat(self, version='007'):
        if version not in self._available_version:
            raise VersionNotFound()
        self._default_version = version

    def setDebug(self, length=100):
        """
        Generate header for Debug
        """
        self._debug_header = length

    def setHeader(self, identifiant='S5', origine='CLI', type_fic='JRL',
                        format_fic='STD', code_ex_clos='', date_bascule=None,
                        date_arrete=None, num_dossier_cab='00001', utilisateur=None,
                        raison_sociale='', reprise='', num_dossier='',
                        frequence='', date_purge=None, sous_version=''):
        if utilisateur is None:
            utilisateur = 'pycegid'

        if date_bascule is None:
            date_bascule = self._default_date

        if date_arrete is None:
            date_arrete = self._default_date

        if date_purge is None:
            date_purge = self._default_date

        self._content['header'] = self._header(identifiant, origine, type_fic,
                                               format_fic, code_ex_clos, date_bascule,
                                               date_arrete, num_dossier_cab, utilisateur,
                                               raison_sociale, reprise, num_dossier,
                                               frequence, date_purge, sous_version)

    def addSAT(self, code='', libelle='', axe='', table1='', table2='',
                     table3='', table4='', table5='', table6='', table7='',
                     table8='', table9='', table10='', abrege='', sens='M'):
        """
        See documentation version 7 page 23/60 which describe "Section Analytique"
        """
        self._content['lines'].append(''.join([
            self._zone_fixe,                   # Prefix (***)
            'SAT',                             # Identifiant
            self._mandatory(code, 17),            # Code
            self._mandatory(libelle, 35),         # Libelle
            self._mandatory(axe, 3),              # Axe
            self._format(table1, 17),          # Table 1
            self._format(table2, 17),          # Table 2
            self._format(table3, 17),          # Table 3
            self._format(table4, 17),          # Table 4
            self._format(table5, 17),          # Table 5
            self._format(table6, 17),          # Table 6
            self._format(table7, 17),          # Table 7
            self._format(table8, 17),          # Table 8
            self._format(table9, 17),          # Table 9
            self._format(table10, 17),         # Table 10
            self._format(abrege, 17),          # Abrege
            self._format(sens, 3),             # Sens
        ]))

    def render(self, filename=''):
        """
        Generate the content, and store it in a file if specified
        """
        if not self._content['header']:
            raise HeaderNotFound()

        content = ''
        if self._debug_header:
            content = self._debug_toolbar()

        content += self._content['header']
        return content

    def _debug_toolbar(self):
        """
        Generate a toolbar to debug position of datas
        """
        header = ''
        for x in range(1, self._debug_header):
            if not x % 10:
                header += '|'
            elif not x % 5:
                header += '.'
            else:
                header += ' '

        header += '\n' + ((self._debug_header - 1) * '-') + '\n'
        return header

    @staticmethod
    def _format(value, length, rpad=False, caract=' '):
        value = str(value)
        if rpad:
            return value.rjust(length, caract)[:length]
        return value.ljust(length, caract)[:length]

    def _mandatory(self, value, length, rpad=False, caract=' '):
        """Check mandary field, if missing raise an error"""
        if not value:
            raise MandatoryException()

        return self._format(value, length, rpad, caract)

    def _header(self, identifiant, origine, type_fic, format_fic, code_ex_clos,
                      date_bascule, date_arrete, num_dossier_cab, utilisateur, raison_sociale,
                      reprise, num_dossier, frequence, date_purge, sous_version):
        """
        Generate the header of the file
        """
        return ''.join([
            self._zone_fixe,                        # Prefix (***)
            self._format(identifiant, 2),           # Identifiant
            self._format(origine, 3),               # Origine Fichier
            self._format(type_fic, 3),              # Type fichier
            self._format(format_fic, 3),            # Foramt de fichier
            self._format(code_ex_clos, 3),          # Code exercice clos
            self._format(date_bascule, 8),          # date de bascule
            self._format(date_arrete, 8),           # date d'arrete periodique
            self._default_version,                  # Version du fichier
            self._format(num_dossier_cab, 5),       # Numero dossier cabinet
            self._format(self._current_date, 12),   # TODO date et heure
            self._format(utilisateur, 35),          # Utilisateur
            self._format(raison_sociale, 35),       # Raison sociale
            self._format(reprise, 4),               # Reprise
            self._format(num_dossier, 6),           # Numero de dossier
            self._format(frequence, 3),             # Frequence
            self._format(date_purge, 8),            # Date de purge des écritures
            self._format(sous_version, 3),          # Sous Version
        ])


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
