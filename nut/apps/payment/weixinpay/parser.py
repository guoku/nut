import xml.etree.cElementTree as ET
import types

from hashlib import md5

from django.utils.encoding import  smart_unicode


from apps.payment.exceptions import PaymentException
from apps.payment.weixinpay.config import WX_APPID, WX_KEY, WX_MCH_ID


class WXResponseParser(object):
    def parse_key_from_response(self, response, key):
        if self.check_wx_response_sign(response) is not True:
            raise PaymentException('wx return sign fail')

        response.encoding='utf-8'
        e = self.parse_string_xml_to_dic(response.text)

        if e.get('return_code') == 'FAIL':
            raise PaymentException('wx payment api interno error %s'
                                   %e.get('return_msg'))

        if e.get('result_code') == 'FAIL':
            raise PaymentException('wx payment get qrcode fail %s'
                                   %e.get('err_code_des'))

        elif e.get('result_code') == 'SUCCESS':
            return e.get(key)

        else:
            raise PaymentException('unkown error')

    def check_wx_response_sign(self, response):
        response.encoding='utf-8'
        params = self.parse_string_xml_to_dic(response.text)
        sign = params.pop('sign', None)
        params, prestr = self.params_filter(params)
        check_sign = self.build_sign(prestr,WX_KEY)
        return sign == check_sign

    def parse_string_xml_to_dic(self, xml_string):
        root  = ET.fromstring(xml_string)
        params = dict()
        if root.tag == 'xml':
            for child in root :
                params[child.tag]=smart_unicode(child.text)
        return params

    def build_sign(self, prestr, api_key):
        signStringTemp = "%s&key=%s"%(prestr,api_key)
        # print(signStringTemp)
        _result= md5(signStringTemp).hexdigest().upper()
        # print(_result)
        return _result

    def params_filter(self, params):
        ks = params.keys()
        ks.sort()
        newparams = {}
        prestr = ''
        for k in ks:
            v = params[k]
            # k = self.smart_str(k, 'utf-8')
            if k not in ('sign','sign_type') and v != '':
                newparams[k] = self.smart_str(v, 'utf-8')
                # newparams[k] = v
                prestr += '%s=%s&' % (k, newparams[k])
        prestr = prestr[:-1]
        # print(prestr)
        return newparams, prestr


    def smart_str(self, s, encoding='utf-8', strings_only=False, errors='strict'):
        """
        Returns a bytestring version of 's', encoded as specified in 'encoding'.
        If strings_only is True, don't convert (some) non-string-like objects.
        """
        if strings_only and isinstance(s, (types.NoneType, int)):
            return s
        if not isinstance(s, basestring):
            try:
                return str(s)
            except UnicodeEncodeError:
                if isinstance(s, Exception):
                    # An Exception subclass containing non-ASCII data that doesn't
                    # know how to print itself properly. We shouldn't raise a
                    # further exception.
                    return ' '.join([self.smart_str(arg, encoding, strings_only,
                            errors) for arg in s])
                return unicode(s).encode(encoding, errors)
        elif isinstance(s, unicode):
            return s.encode(encoding, errors)
        elif s and encoding != 'utf-8':
            return s.decode('utf-8', errors).encode(encoding, errors)
        else:
            return s