#! /usr/bin/python

# PurePythonGeoIP.py
#
# Copyright (C) 2005 Guwashi <guwashi[AT]fooos[DOT]com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# This code is based on
# http://www.maxmind.com/app/python
# http://www.maxmind.com/download/geoip/api/pureperl

import re
import struct

PUREPYTHONGEOIP_VERSION = '1.0.0'

def nreverse(sequence):
    '''nreverse in Common Lisp. :)'''
    sequence.reverse()
    return sequence

class GeoIP:
    __STANDARD_RECORD_LENGTH = 3
    __GEOIP_COUNTRY_EDITION = 106
    __GEOIP_COUNTRY_BEGIN = 16776960

    __COUNTRIES = ('--','AP','EU','AD','AE','AF','AG','AI','AL','AM','AN','AO','AQ','AR','AS','AT','AU','AW','AZ','BA','BB','BD','BE','BF','BG','BH','BI','BJ','BM','BN','BO','BR','BS','BT','BV','BW','BY','BZ','CA','CC','CD','CF','CG','CH','CI','CK','CL','CM','CN','CO','CR','CU','CV','CX','CY','CZ','DE','DJ','DK','DM','DO','DZ','EC','EE','EG','EH','ER','ES','ET','FI','FJ','FK','FM','FO','FR','FX','GA','GB','GD','GE','GF','GH','GI','GL','GM','GN','GP','GQ','GR','GS','GT','GU','GW','GY','HK','HM','HN','HR','HT','HU','ID','IE','IL','IN','IO','IQ','IR','IS','IT','JM','JO','JP','KE','KG','KH','KI','KM','KN','KP','KR','KW','KY','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','LY','MA','MC','MD','MG','MH','MK','ML','MM','MN','MO','MP','MQ','MR','MS','MT','MU','MV','MW','MX','MY','MZ','NA','NC','NE','NF','NG','NI','NL','NO','NP','NR','NU','NZ','OM','PA','PE','PF','PG','PH','PK','PL','PM','PN','PR','PS','PT','PW','PY','QA','RE','RO','RU','RW','SA','SB','SC','SD','SE','SG','SH','SI','SJ','SK','SL','SM','SN','SO','SR','ST','SV','SY','SZ','TC','TD','TF','TG','TH','TJ','TK','TM','TN','TO','TP','TR','TT','TV','TW','TZ','UA','UG','UM','US','UY','UZ','VA','VC','VE','VG','VI','VN','VU','WF','WS','YE','YT','YU','ZA','ZM','ZR','ZW','A1','A2')
    __CODE3S = ('--','AP','EU','AND','ARE','AFG','ATG','AIA','ALB','ARM','ANT','AGO','AQ','ARG','ASM','AUT','AUS','ABW','AZE','BIH','BRB','BGD','BEL','BFA','BGR','BHR','BDI','BEN','BMU','BRN','BOL','BRA','BHS','BTN','BV','BWA','BLR','BLZ','CAN','CC','COD','CAF','COG','CHE','CIV','COK','CHL','CMR','CHN','COL','CRI','CUB','CPV','CX','CYP','CZE','DEU','DJI','DNK','DMA','DOM','DZA','ECU','EST','EGY','ESH','ERI','ESP','ETH','FIN','FJI','FLK','FSM','FRO','FRA','FX','GAB','GBR','GRD','GEO','GUF','GHA','GIB','GRL','GMB','GIN','GLP','GNQ','GRC','GS','GTM','GUM','GNB','GUY','HKG','HM','HND','HRV','HTI','HUN','IDN','IRL','ISR','IND','IO','IRQ','IRN','ISL','ITA','JAM','JOR','JPN','KEN','KGZ','KHM','KIR','COM','KNA','PRK','KOR','KWT','CYM','KAZ','LAO','LBN','LCA','LIE','LKA','LBR','LSO','LTU','LUX','LVA','LBY','MAR','MCO','MDA','MDG','MHL','MKD','MLI','MMR','MNG','MAC','MNP','MTQ','MRT','MSR','MLT','MUS','MDV','MWI','MEX','MYS','MOZ','NAM','NCL','NER','NFK','NGA','NIC','NLD','NOR','NPL','NRU','NIU','NZL','OMN','PAN','PER','PYF','PNG','PHL','PAK','POL','SPM','PCN','PRI','PSE','PRT','PLW','PRY','QAT','REU','ROM','RUS','RWA','SAU','SLB','SYC','SDN','SWE','SGP','SHN','SVN','SJM','SVK','SLE','SMR','SEN','SOM','SUR','STP','SLV','SYR','SWZ','TCA','TCD','TF','TGO','THA','TJK','TKL','TLS','TKM','TUN','TON','TUR','TTO','TUV','TWN','TZA','UKR','UGA','UM','USA','URY','UZB','VAT','VCT','VEN','VGB','VIR','VNM','VUT','WLF','WSM','YEM','YT','YUG','ZAF','ZMB','ZR','ZWE','A1','A2')
    __NAMES = ("--","Asia/Pacific Region","Europe","Andorra","United Arab Emirates","Afghanistan","Antigua and Barbuda","Anguilla","Albania","Armenia","Netherlands Antilles","Angola","Antarctica","Argentina","American Samoa","Austria","Australia","Aruba","Azerbaijan","Bosnia and Herzegovina","Barbados","Bangladesh","Belgium","Burkina Faso","Bulgaria","Bahrain","Burundi","Benin","Bermuda","Brunei Darussalam","Bolivia","Brazil","Bahamas","Bhutan","Bouvet Island","Botswana","Belarus","Belize","Canada","Cocos (Keeling) Islands","Congo, The Democratic Republic of the","Central African Republic","Congo","Switzerland","Cote D'Ivoire","Cook Islands","Chile","Cameroon","China","Colombia","Costa Rica","Cuba","Cape Verde","Christmas Island","Cyprus","Czech Republic","Germany","Djibouti","Denmark","Dominica","Dominican Republic","Algeria","Ecuador","Estonia","Egypt","Western Sahara","Eritrea","Spain","Ethiopia","Finland","Fiji","Falkland Islands (Malvinas)","Micronesia, Federated States of","Faroe Islands","France","France, Metropolitan","Gabon","United Kingdom","Grenada","Georgia","French Guiana","Ghana","Gibraltar","Greenland","Gambia","Guinea","Guadeloupe","Equatorial Guinea","Greece","South Georgia and the South Sandwich Islands","Guatemala","Guam","Guinea-Bissau","Guyana","Hong Kong","Heard Island and McDonald Islands","Honduras","Croatia","Haiti","Hungary","Indonesia","Ireland","Israel","India","British Indian Ocean Territory","Iraq","Iran, Islamic Republic of","Iceland","Italy","Jamaica","Jordan","Japan","Kenya","Kyrgyzstan","Cambodia","Kiribati","Comoros","Saint Kitts and Nevis",
"Korea, Democratic People's Republic of","Korea, Republic of","Kuwait","Cayman Islands","Kazakhstan","Lao People's Democratic Republic","Lebanon","Saint Lucia","Liechtenstein","Sri Lanka","Liberia","Lesotho","Lithuania","Luxembourg","Latvia","Libyan Arab Jamahiriya","Morocco","Monaco","Moldova, Republic of","Madagascar","Marshall Islands","Macedonia","Mali","Myanmar","Mongolia","Macau","Northern Mariana Islands","Martinique","Mauritania","Montserrat","Malta","Mauritius","Maldives","Malawi","Mexico","Malaysia","Mozambique","Namibia","New Caledonia","Niger","Norfolk Island","Nigeria","Nicaragua","Netherlands","Norway","Nepal","Nauru","Niue","New Zealand","Oman","Panama","Peru","French Polynesia","Papua New Guinea","Philippines","Pakistan","Poland","Saint Pierre and Miquelon","Pitcairn Islands","Puerto Rico","Palestinian Territory, Occupied","Portugal","Palau","Paraguay","Qatar","Reunion","Romania","Russian Federation","Rwanda","Saudi Arabia","Solomon Islands","Seychelles","Sudan","Sweden","Singapore","Saint Helena","Slovenia","Svalbard and Jan Mayen","Slovakia","Sierra Leone","San Marino","Senegal","Somalia","Suriname","Sao Tome and Principe","El Salvador","Syrian Arab Republic","Swaziland","Turks and Caicos Islands","Chad","French Southern Territories","Togo","Thailand","Tajikistan","Tokelau","Turkmenistan","Tunisia","Tonga","East Timor","Turkey","Trinidad and Tobago","Tuvalu","Taiwan","Tanzania, United Republic of","Ukraine","Uganda","United States Minor Outlying Islands","United States","Uruguay","Uzbekistan","Holy See (Vatican City State)","Saint Vincent and the Grenadines","Venezuela","Virgin Islands, British","Virgin Islands, U.S.","Vietnam","Vanuatu","Wallis and Futuna","Samoa","Yemen","Mayotte","Yugoslavia","South Africa","Zambia","Zaire","Zimbabwe",
"Anonymous Proxy","Satellite Provider")

    __RE_IP_DOTTED_FORM = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

    GEOIP_STANDARD = 0 # TODO

    def addr_to_num(ip_address):
        '''Convert IP-address to number.'''
        # a = [int(s) for s in re.split('\.', ip_address)]
        a = map(int, re.split('\.', ip_address))
        return a[0] * 16777216L + a[1] * 65536L + a[2] * 256L + a[3]

    def open(db_file, flags):
        '''Create a new GeoIP object.'''
        gi = GeoIP()
        gi.db_file = db_file
        gi.flags = flags # TODO
        gi.fh = open(db_file, 'r')
        gi.databaseType = GeoIP.__GEOIP_COUNTRY_EDITION # TODO
        gi.record_length = GeoIP.__STANDARD_RECORD_LENGTH # TODO
        gi.databaseSegments = GeoIP.__GEOIP_COUNTRY_BEGIN # TODO
        return gi

    def new(flags):
        '''Create a new GeoIP object.'''
        return GeoIP.open('/usr/local/share/GeoIP/GeoIP.dat', flags)

    def __seek_country(self, ipnum):
        '''Seek GeoIP data file to find country id.'''
        fh = self.fh
        record_length = self.record_length
        databaseSegments = self.databaseSegments
        offset = 0
        x0 = -1
        x1 = -1
        for depth in nreverse(range(32)):
            fh.seek(offset * 2 * record_length, 0)
            x0 = fh.read(record_length)
            x1 = fh.read(record_length)
            x0, = struct.unpack("<1l", x0 + "\0")
            x1, = struct.unpack("<1l", x1 + "\0")
            if ipnum & (1L << depth):
                if x1 >= databaseSegments:
                    return x1
                offset = x1
            else:
                if x0 >= databaseSegments:
                    return x0
                offset = x0
        raise Exception('Error Traversing Database for ipnum = %d - Perhaps database is corrupt?' % ipnum) # TODO

    def id_by_addr(self, ip_address):
        '''Find country id by IP-address.'''
        if self.__RE_IP_DOTTED_FORM.match(ip_address):
            return self.__seek_country(self.addr_to_num(ip_address)) - self.__GEOIP_COUNTRY_BEGIN
        else:
            return 0

    def id_to_country_code(id):
        '''Convert country id to country code.'''
        return GeoIP.__COUNTRIES[id]

    def id_to_country_code3(id):
        '''Convert country id to country code.'''
        return GeoIP.__CODE3S[id]

    def id_to_country_name(id):
        '''Convert country id to country code.'''
        return GeoIP.__NAMES[id]

    def country_code_by_addr(self, ip_address):
        '''Find country code by IP-address.'''
        return GeoIP.id_to_country_code(self.id_by_addr(ip_address))

    def country_code3_by_addr(self, ip_address):
        '''Find country code3 by IP-address.'''
        return GeoIP.id_to_country_code3(self.id_by_addr(ip_address))

    def country_name_by_addr(self, ip_address):
        '''Find country name by IP-address.'''
        return GeoIP.id_to_country_name(self.id_by_addr(ip_address))

    addr_to_num = staticmethod(addr_to_num)
    open = staticmethod(open)
    new = staticmethod(new)
    id_to_country_code = staticmethod(id_to_country_code)
    id_to_country_code3 = staticmethod(id_to_country_code3)
    id_to_country_name = staticmethod(id_to_country_name)

if '__main__' == __name__:
    import sys
    import string

    argc = len(sys.argv)
    gi = None
    if 2 == argc:
        gi = GeoIP.new(GeoIP.GEOIP_STANDARD)
    elif 3 == argc:
        gi = GeoIP.open(sys.argv[2], GeoIP.GEOIP_STANDARD)
    else:
        print "Usage:\n  %s <ipaddress> [geoipdatafile]" % sys.argv[0]
        sys.exit(1)

    ip = sys.argv[1]
    id = str(gi.id_by_addr(ip))
    code = gi.country_code_by_addr(ip)
    code3 = gi.country_code3_by_addr(ip)
    name = gi.country_name_by_addr(ip)

    print string.join(['ipaddress', 'id', 'code', 'code3', 'name'], "\t")
    print string.join([ip, id, code, code3, name], "\t")
