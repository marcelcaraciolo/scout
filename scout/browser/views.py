# -*- coding: utf-8 -*-
from flask import abort, Blueprint, jsonify, redirect, request

from ..extensions import store
from ..helpers import get_document_or_404, send_file_partial
from ..models import Case
from .utils import build_igv_url

browser = Blueprint('browser', __name__, template_folder='templates')


@browser.route('/remote/static/<path:path>', methods=['OPTIONS', 'GET'])
def remote_static(path):
  """Stream *large* static files with special requirements."""
  # new_resp.status_code = resp.status_code
  # new_resp.headers['content-length'] = resp.headers.get('content-length')
  # new_resp.headers['accept-ranges'] = resp.headers.get('accept-ranges')
  # new_resp.headers['Content-Type'] = 'application/octet-stream'
  range_header = request.headers.get('Range', None)
  if not range_header and path.endswith('.bam'):
    return abort(500)

  return send_file_partial('/' + path)


@browser.route('/<institute_id>/<case_id>/<variant_id>/igv')
def igv_init(institute_id, case_id, variant_id):
  """Redicect user to start an IGV session based on a variant."""
  case = get_document_or_404(Case, case_id)
  variant = store.variant(document_id=variant_id)

  # sanity check to see if there's any reason to launch IGV
  if variant is None:
    return jsonify(error='Variant not found'), 406

  # figure out where the variant/indel ends
  variant_end = variant.position + len(variant.alternative) - 1

  # compose URL
  igv_url = build_igv_url(variant.chromosome, variant.position, variant_end,
                          case.vcf_file, case.bam_files)

  return redirect(igv_url)